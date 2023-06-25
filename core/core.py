from datetime import datetime
from typing import List

from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from db import Car, Reservation
from schemas import ReservationCarsSchema


def get_available_car(session: Session, start_timestamp: int, end_timestamp: int) -> Car | None:
    """Finds available car for desired timeslot, no overlaps

    Args:
        session (Session): db session
        start_timestamp (int): unix timestamp of the reservation start
        end_timestamp (int): unix timestamp of the reservation end

    Returns:
        Car | None: Car object if found
    """
    return (
        session.query(Car)
        .filter(
            ~Car.reservations.any(
                or_(
                    and_(Reservation.start_timestamp <= start_timestamp, Reservation.end_timestamp > start_timestamp),
                    and_(Reservation.start_timestamp < end_timestamp, Reservation.end_timestamp >= end_timestamp),
                    and_(Reservation.start_timestamp >= start_timestamp, Reservation.end_timestamp <= end_timestamp),
                )
            )
        )
        .first()
    )


def get_all_upcoming_reservations(session: Session) -> List[ReservationCarsSchema]:
    """queries all upcoming reservations and returns them as a list

    Args:
        session (Session): db session

    Returns:
        List[ReservationCarsSchema]: list of reservations
    """
    current_timestamp = int(datetime.now().timestamp())
    # query all upcoming reservations
    upcoming_reservations = session.query(Reservation).filter(Reservation.start_timestamp >= current_timestamp).all()
    result = []
    for reservation in upcoming_reservations:
        car: Car = reservation.car
        result.append(
            ReservationCarsSchema(
                timestamp_start=reservation.start_timestamp,
                timestamp_end=reservation.end_timestamp,
                car_uid=car.uid,
                car_maker=car.maker,
                car_model=car.model,
            )
        )
    return result

from typing import List
from datetime import datetime
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

import core
from db import Car, Reservation, session_manager
from schemas import BasicResponseSchema, ReservationSchema, SuccessfulReservationSchema, ReservationCarsSchema

router = APIRouter(prefix="/reservation")


@router.post(
    "/make_reservation",
    status_code=status.HTTP_201_CREATED,
    response_model=SuccessfulReservationSchema,
    responses={
        status.HTTP_201_CREATED: {"model": SuccessfulReservationSchema},
        status.HTTP_400_BAD_REQUEST: {"model": BasicResponseSchema},
        status.HTTP_404_NOT_FOUND: {"model": BasicResponseSchema},
    }
)
def make_reservation(
    reservation: ReservationSchema,
    session: Session = Depends(session_manager)
) -> SuccessfulReservationSchema:
    """Makes a new reservation in available timeslot"""
    core.validate_reservation_time(reservation.timestamp_start, reservation.timestamp_end)
    # query first available car
    available_car = session.query(Car).filter() # TODO
    if not available_car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No Car found for this timeslot"
        )
    reservation_obj = Reservation(
        start_timestamp=reservation.timestamp_start,
        end_timestamp=reservation.timestamp_end
    )
    available_car.reservations.append(reservation_obj)
    return SuccessfulReservationSchema(
        start = datetime.fromtimestamp(reservation.timestamp_start),
        end = datetime.fromtimestamp(reservation.timestamp_end),
        duration = (reservation.timestamp_end - reservation.timestamp_start) / 3600,
        car_uid = available_car.uid,
        car_maker = available_car.maker,
        car_model = available_car.model
    )


@router.get(
    "/reservations",
    response_model=List[ReservationCarsSchema],
    responses={
        status.HTTP_200_OK: {"model": List[ReservationCarsSchema]},
    }
)
def get_all_reservations(session: Session = Depends(session_manager)) -> List[ReservationCarsSchema]:
    """gets all upcomming reservations

    Args:
        session (Session, optional): db session

    Returns:
        List[ReservationCars]: list of all reservations and their related cars
    """
    current_timestamp = int(datetime.now().timestamp())
    # query all upcoming reservations
    upcoming_reservations = session.query(Reservation).filter(Reservation.start_timestamp >= current_timestamp).all()
    result = []
    for reservation in upcoming_reservations:
        car: Car = reservation.car
        result.append(ReservationCarsSchema(
            timestamp_start=reservation.start_timestamp,
            timestamp_end=reservation.end_timestamp,
            car_uid=car.uid,
            car_maker=car.maker,
            car_model=car.model,
        ))
    return result
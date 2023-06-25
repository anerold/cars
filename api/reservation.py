from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import core
from db import Reservation, session_manager
from schemas import BasicResponseSchema, ReservationCarsSchema, ReservationSchema, SuccessfulReservationSchema

router = APIRouter(prefix="/reservation")


@router.post(
    "/make_reservation",
    status_code=status.HTTP_201_CREATED,
    response_model=SuccessfulReservationSchema,
    responses={
        status.HTTP_201_CREATED: {"model": SuccessfulReservationSchema},
        status.HTTP_400_BAD_REQUEST: {"model": BasicResponseSchema},
        status.HTTP_404_NOT_FOUND: {"model": BasicResponseSchema},
    },
)
def make_reservation(
    reservation: ReservationSchema, session: Session = Depends(session_manager)
) -> SuccessfulReservationSchema:
    """Makes a new reservation in available timeslot"""
    core.validate_reservation_time(reservation.timestamp_start, reservation.timestamp_end)
    # get first available car
    available_car = core.get_available_car(session, reservation.timestamp_start, reservation.timestamp_end)
    if not available_car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Car found for this timeslot")
    # make the reservation
    reservation_obj = Reservation(start_timestamp=reservation.timestamp_start, end_timestamp=reservation.timestamp_end)
    available_car.reservations.append(reservation_obj)
    return SuccessfulReservationSchema(
        start=datetime.fromtimestamp(reservation.timestamp_start),
        end=datetime.fromtimestamp(reservation.timestamp_end),
        duration=(reservation.timestamp_end - reservation.timestamp_start) / 3600,
        car_uid=available_car.uid,
        car_maker=available_car.maker,
        car_model=available_car.model,
    )


@router.get(
    "/reservations",
    response_model=List[ReservationCarsSchema],
    responses={
        status.HTTP_200_OK: {"model": List[ReservationCarsSchema]},
    },
)
def get_all_reservations(session: Session = Depends(session_manager)) -> List[ReservationCarsSchema]:
    """Gets all upcomming reservations"""
    return core.get_all_upcoming_reservations(session)

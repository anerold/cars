from datetime import datetime, timedelta

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

import config
from db import Car


def validate_car_uid(car_uid: str) -> None:
    """Validates if provided string is valid car_uid

    Args:
        car_uid (str): string to be evaluated

    Raises:
        HTTPException: if invalid
    """
    if not (2 <= len(car_uid) <= 10 and car_uid[0] == "C" and car_uid[1:].isnumeric()):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{car_uid} is not a valid uid. Please use C<number up to 9 digits> format",
        )


def validate_reservation_time(start_timestamp: int, end_timestamp: int) -> None:
    """Validates if reservation time is max config.RESERVATION_MAX_DURATON_HOURS hours
       and not more than config.RESERVATION_MAX_IN_FUTURE_HOURS hours in the future

    Args:
        start_timestamp (int): start of reservation
        end_timestamp (int): end of reservation
    """
    now = datetime.now()
    start = datetime.fromtimestamp(start_timestamp)
    end = datetime.fromtimestamp(end_timestamp)
    errors = []
    if start >= end:
        errors.append("Start time cannot be equal or larger than End time")
    if start < now:
        errors.append("Start time cannot be in the past")
    if (end - start).total_seconds() / 3600 > config.RESERVATION_MAX_DURATON_HOURS:
        errors.append("Reservation time cannot be longer than 2 hours")
    if start > now + timedelta(hours=config.RESERVATION_MAX_IN_FUTURE_HOURS):
        errors.append("Reservation Start Time cannot be more than 24 hours in the future")
    if errors:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="\n".join(errors))


def raise_for_already_exists(car_uid: str, session: Session) -> None:
    """raises HTTPException with status 409 is record with car_uid exists in the cars table

    Args:
        car_uid (str): car uid to be checked
        session (Session): db session

    Raises:
        HTTPException: if exists
    """
    if session.query(Car).filter_by(uid=car_uid).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Car with uid {car_uid} already exists",
        )


def raise_for_not_exists(car: Car | None, car_uid):
    """raises HTTPException with status 404 is record with car_uid doesn't exists in the cars table


    Args:
        car (Car | None): Car object
        car_uid (_type_): car uid to bechecked

    Raises:
        HTTPException: if does not exist
    """
    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Car with uid {car_uid} not found",
        )

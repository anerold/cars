from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

import core
from db import Car, session_manager
from schemas import BasicResponseSchema, CarDeleteSchema, CarSchema, CarUpdateSchema

router = APIRouter(prefix="/car")


@router.post(
    "/add",
    status_code=status.HTTP_201_CREATED,
    response_model=BasicResponseSchema,
    responses={
        status.HTTP_201_CREATED: {"model": BasicResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"model": BasicResponseSchema},
        status.HTTP_409_CONFLICT: {"model": BasicResponseSchema},
    },
)
def add_car(
    car_info: CarSchema,
    session: Session = Depends(session_manager),
) -> BasicResponseSchema:
    """Adds a new car to DB"""
    core.raise_for_already_exists(car_info.uid, session)
    core.validate_car_uid(car_info.uid)
    session.add(Car(uid=car_info.uid, maker=car_info.maker, model=car_info.model))
    return BasicResponseSchema(detail="New car created")


@router.put(
    "/update",
    response_model=BasicResponseSchema,
    responses={
        status.HTTP_200_OK: {"model": BasicResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"model": BasicResponseSchema},
        status.HTTP_404_NOT_FOUND: {"model": BasicResponseSchema},
    },
)
def update_car(
    car_info: CarUpdateSchema,
    session: Session = Depends(session_manager),
) -> BasicResponseSchema:
    """Updates a car"""
    core.raise_for_already_exists(car_info.new_uid, session)
    car_to_be_updated = session.query(Car).filter_by(uid=car_info.uid).first()
    core.raise_for_not_exists(car_to_be_updated, car_info.uid)
    if car_info.new_uid:
        core.validate_car_uid(car_info.new_uid)
    car_to_be_updated.uid = car_info.new_uid if car_info.new_uid else car_to_be_updated.uid
    car_to_be_updated.maker = car_info.new_maker if car_info.new_maker else car_to_be_updated.maker
    car_to_be_updated.model = car_info.new_model if car_info.new_model else car_to_be_updated.model
    return BasicResponseSchema(detail="Car updated successfully")


@router.delete(
    "/remove",
    response_model=BasicResponseSchema,
    responses={
        status.HTTP_200_OK: {"model": BasicResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"model": BasicResponseSchema},
    },
)
def remove_car(
    car_info: CarDeleteSchema,
    session: Session = Depends(session_manager),
) -> BasicResponseSchema:
    """Removes a car"""
    car_to_be_deleted = session.query(Car).filter_by(uid=car_info.uid).first()
    core.raise_for_not_exists(car_to_be_deleted, car_info.uid)
    session.delete(car_to_be_deleted)
    return BasicResponseSchema(detail="Car deleted successfully")


@router.get(
    "/cars",
    response_model=List[CarSchema],
    responses={
        status.HTTP_200_OK: {"model": List[CarSchema]},
    },
)
def get_all_cars(session: Session = Depends(session_manager)) -> List[CarSchema]:
    """Returns list of all cars"""
    cars = session.query(Car).all()
    result = []
    for car in cars:
        result.append(CarSchema(uid=car.uid, maker=car.maker, model=car.model))
    return result

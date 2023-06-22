from typing import List

from fastapi import APIRouter, status, Depends, Response, Request, HTTPException
from sqlalchemy.orm import Session

from schemas import BasicResponse, Car as CarSchema
from db import session_manager, Car
import core

router = APIRouter(prefix="/car")



@router.post(
    "/add",
    status_code=status.HTTP_201_CREATED,
    response_model=BasicResponse,
    responses={
        status.HTTP_201_CREATED: {"model": BasicResponse},
        status.HTTP_400_BAD_REQUEST: {"model": BasicResponse},
        status.HTTP_409_CONFLICT: {"model": BasicResponse},
    }
)
def add_car(
    car_info: CarSchema,
    session: Session = Depends(session_manager),
) -> BasicResponse:
    """Adds a new car to DB

    Args:
        car_info (CarSchema): request body
        session (Session, optional): db session

    Raises:
        HTTPException: when malformed request od car with this uid already exists

    Returns:
        BasicResponse: new car created
    """
    if session.query(Car).filter_by(uid = car_info.uid).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Car with uid {car_info.uid} already exists")
    core.validate_car_uid(car_info.uid)
    session.add(Car(uid=car_info.uid, maker=car_info.maker, model=car_info.model))
    return BasicResponse(detail="New car created")
    


@router.put(
    "/update",
    response_model=BasicResponse,
    responses={
        status.HTTP_200_OK: {"model": BasicResponse},
        status.HTTP_400_BAD_REQUEST: {"model": BasicResponse},
    }
)
def update_car():
    pass

@router.delete(
    "/remove",
    response_model=BasicResponse,
    responses={
        status.HTTP_200_OK: {"model": BasicResponse},
        status.HTTP_400_BAD_REQUEST: {"model": BasicResponse},
    }
)
def remove_car():
    pass

@router.get(
    "/cars",
    response_model=List[CarSchema],
    responses={
        status.HTTP_200_OK: {"model": List[CarSchema]},
        status.HTTP_404_NOT_FOUND: {"model": BasicResponse},
    }
)
def get_all_cars():
    pass
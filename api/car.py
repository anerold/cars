from typing import List
from fastapi import APIRouter, status

from schemas import BasicResponse, Car

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
def add_car():
    pass


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
    response_model=List[Car],
    responses={
        status.HTTP_200_OK: {"model": List[Car]},
        status.HTTP_404_NOT_FOUND: {"model": BasicResponse},
    }
)
def get_all_cars():
    pass
from typing import List
from fastapi import APIRouter, status

from schemas import BasicResponse, Reservation

router = APIRouter(prefix="/reservation")


@router.post(
    "/make_reservation",
    status_code=status.HTTP_201_CREATED,
    response_model=BasicResponse,
    responses={
        status.HTTP_201_CREATED: {"model": BasicResponse},
        status.HTTP_400_BAD_REQUEST: {"model": BasicResponse},
    }
)
def make_reservation():
    pass

@router.get(
    "/reservations",
    response_model=List[Reservation],
    responses={
        status.HTTP_200_OK: {"model": List[Reservation]},
        status.HTTP_404_NOT_FOUND: {"model": BasicResponse},
    }
)
def get_all_reservations():
    pass
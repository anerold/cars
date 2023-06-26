from datetime import datetime

from pydantic import BaseModel


class ReservationSchema(BaseModel):
    """Schema representing one reservation"""

    timestamp_start: int
    timestamp_end: int


class ReservationCarsSchema(BaseModel):
    """Schema representing one reservation with info about related car"""

    timestamp_start: int
    timestamp_end: int
    car_uid: str
    car_maker: str
    car_model: str


class SuccessfulReservationSchema(BaseModel):
    """Schema containing info about newly created reservation"""

    start: datetime
    end: datetime
    duration: float
    car_uid: str
    car_maker: str
    car_model: str

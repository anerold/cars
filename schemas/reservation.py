from pydantic import BaseModel

class Reservation(BaseModel):
    """Schema representing one reservation"""
    timestamp_start: int
    timestamp_end: int
    car_uid: str
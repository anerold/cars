from pydantic import BaseModel


class Car(BaseModel):
    """Schema representing one car"""
    maker: str
    model: str
    uid: str
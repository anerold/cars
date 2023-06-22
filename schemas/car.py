from pydantic import BaseModel
from typing import Optional


class CarSchema(BaseModel):
    """Schema representing one car"""
    uid: str
    maker: str
    model: str

class CarUpdateSchema(BaseModel):
    uid: str
    new_uid: Optional[str]
    new_maker: Optional[str]
    new_model: Optional[str]

class CarDeleteSchema(BaseModel):
    uid: str
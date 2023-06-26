from typing import Optional

from pydantic import BaseModel


class CarSchema(BaseModel):
    """Schema representing one car"""

    uid: str
    maker: str
    model: str


class CarUpdateSchema(BaseModel):
    """Schema representing one car to be updated"""

    uid: str
    new_uid: Optional[str]
    new_maker: Optional[str]
    new_model: Optional[str]


class CarDeleteSchema(BaseModel):
    """Schema representing one car to be deleted"""

    uid: str

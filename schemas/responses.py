from pydantic import BaseModel


class BasicResponseSchema(BaseModel):
    """Basic response to request"""

    detail: str

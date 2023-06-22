from pydantic import BaseModel

class BasicResponse(BaseModel):
    """Basic response to request"""
    detail: str
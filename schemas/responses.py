from pydantic import BaseModel

class BasicResponse(BaseModel):
    """Basic response to request"""
    status: str
    message: str
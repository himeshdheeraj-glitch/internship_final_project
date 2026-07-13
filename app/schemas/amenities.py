from typing import Optional
from pydantic import BaseModel, Field
from app.shared.schemas import BaseResponseSchema

class AmenityCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=255)

class AmenityUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=255)

class AmenityResponse(BaseResponseSchema):
    name: str
    description: Optional[str] = None

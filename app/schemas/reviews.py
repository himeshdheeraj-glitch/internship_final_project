import uuid
from typing import Optional
from pydantic import BaseModel, Field
from app.shared.schemas import BaseResponseSchema
from app.schemas.users import UserResponse

class ReviewCreate(BaseModel):
    property_id: uuid.UUID
    rating: int = Field(..., ge=1, le=5)
    comment: str = Field(..., min_length=5, max_length=1000)

class ReviewUpdate(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=5)
    comment: Optional[str] = Field(None, min_length=5, max_length=1000)

class ReviewResponse(BaseResponseSchema):
    user_id: uuid.UUID
    property_id: uuid.UUID
    rating: int
    comment: str
    user: Optional[UserResponse] = None

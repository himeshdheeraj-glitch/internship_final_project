import uuid
from typing import Optional
from pydantic import BaseModel
from app.shared.schemas import BaseResponseSchema
from app.schemas.properties import PropertyResponse

class FavoriteCreate(BaseModel):
    property_id: uuid.UUID

class FavoriteResponse(BaseResponseSchema):
    user_id: uuid.UUID
    property_id: uuid.UUID
    property: Optional[PropertyResponse] = None

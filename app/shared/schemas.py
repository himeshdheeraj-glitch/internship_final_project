import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class BaseResponseSchema(BaseModel):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class MessageResponse(BaseModel):
    message: str

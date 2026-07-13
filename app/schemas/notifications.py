import uuid
from pydantic import BaseModel
from app.shared.schemas import BaseResponseSchema

class NotificationCreate(BaseModel):
    user_id: uuid.UUID
    title: str
    message: str
    type: str = "info"

class NotificationResponse(BaseResponseSchema):
    user_id: uuid.UUID
    title: str
    message: str
    type: str
    is_read: bool

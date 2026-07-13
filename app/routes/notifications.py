import uuid
from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.shared.responses import APIResponse
from app.core.dependencies import get_current_user
from app.models.users import User
from app.schemas.notifications import NotificationResponse
from app.services.notifications import notification_service

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get("", response_model=APIResponse[List[NotificationResponse]])
async def get_my_notifications(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    notifs = await notification_service.get_user_notifications(db, user_id=current_user.id)
    return APIResponse(message="Notifications retrieved", data=notifs)

@router.post("/{notification_id}/read", response_model=APIResponse[NotificationResponse])
async def read_notification(notification_id: uuid.UUID, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    notif = await notification_service.mark_as_read(db, notification_id=notification_id, user_id=current_user.id)
    return APIResponse(message="Notification marked as read", data=notif)

@router.post("/read-all", response_model=APIResponse[None])
async def read_all_notifications(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    await notification_service.mark_all_as_read(db, user_id=current_user.id)
    return APIResponse(message="All notifications marked as read")

import uuid
from typing import List
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import NotFoundException, ForbiddenException
from app.models.notifications import Notification

class NotificationService:
    async def send_notification(
        self, db: AsyncSession, *, user_id: uuid.UUID, title: str, message: str, type: str = "info"
    ) -> Notification:
        db_obj = Notification(user_id=user_id, title=title, message=message, type=type, is_read=False)
        db.add(db_obj)
        await db.flush()
        return db_obj

    async def get_user_notifications(self, db: AsyncSession, *, user_id: uuid.UUID) -> List[Notification]:
        query = select(Notification).where(Notification.user_id == user_id).order_by(Notification.created_at.desc())
        result = await db.execute(query)
        return list(result.scalars().all())

    async def mark_as_read(self, db: AsyncSession, *, notification_id: uuid.UUID, user_id: uuid.UUID) -> Notification:
        query = select(Notification).where(Notification.id == notification_id)
        res = await db.execute(query)
        notif = res.scalars().first()
        if not notif:
            raise NotFoundException(message="Notification not found")
        if notif.user_id != user_id:
            raise ForbiddenException(message="Unauthorized access")
        notif.is_read = True
        db.add(notif)
        await db.flush()
        return notif

    async def mark_all_as_read(self, db: AsyncSession, *, user_id: uuid.UUID) -> None:
        stmt = update(Notification).where(
            Notification.user_id == user_id,
            Notification.is_read == False
        ).values(is_read=True)
        await db.execute(stmt)
        await db.flush()

notification_service = NotificationService()

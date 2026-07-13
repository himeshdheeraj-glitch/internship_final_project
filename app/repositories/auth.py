import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.auth import RefreshToken, AuditLog
from app.models.users import User

class AuthRepository:
    async def get_refresh_token(self, db: AsyncSession, token: str) -> Optional[RefreshToken]:
        query = select(RefreshToken).where(
            RefreshToken.token == token,
            RefreshToken.is_revoked == False
        ).options(selectinload(RefreshToken.user).selectinload(User.role))
        result = await db.execute(query)
        return result.scalars().first()

    async def create_refresh_token(
        self, db: AsyncSession, *, user_id: uuid.UUID, token: str, expires_at: datetime
    ) -> RefreshToken:
        db_obj = RefreshToken(user_id=user_id, token=token, expires_at=expires_at)
        db.add(db_obj)
        await db.flush()
        return db_obj

    async def revoke_refresh_tokens(self, db: AsyncSession, user_id: uuid.UUID) -> None:
        query = update(RefreshToken).where(
            RefreshToken.user_id == user_id,
            RefreshToken.is_revoked == False
        ).values(is_revoked=True)
        await db.execute(query)
        await db.flush()

    async def create_audit_log(
        self,
        db: AsyncSession,
        *,
        user_id: Optional[uuid.UUID],
        action: str,
        table_name: str,
        record_id: Optional[uuid.UUID] = None,
        old_values: Optional[dict] = None,
        new_values: Optional[dict] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> AuditLog:
        db_obj = AuditLog(
            user_id=user_id,
            action=action,
            table_name=table_name,
            record_id=record_id,
            old_values=old_values,
            new_values=new_values,
            ip_address=ip_address,
            user_agent=user_agent
        )
        db.add(db_obj)
        await db.flush()
        return db_obj

auth_repository = AuthRepository()

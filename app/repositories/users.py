import uuid
from typing import Optional, List
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.users import User, Role
from app.shared.base_repository import BaseRepository

class UserRepository(BaseRepository[User]):
    def __init__(self) -> None:
        super().__init__(User)

    async def get_by_email(self, db: AsyncSession, email: str) -> Optional[User]:
        normalized_email = email.strip().lower()
        query = select(User).where(
            func.lower(User.email) == normalized_email,
            User.deleted_at == None
        ).options(selectinload(User.role))
        result = await db.execute(query)
        return result.scalars().first()

    async def get_user_with_role(self, db: AsyncSession, user_id: uuid.UUID) -> Optional[User]:
        query = select(User).where(User.id == user_id, User.deleted_at == None).options(
            selectinload(User.role)
        )
        result = await db.execute(query)
        return result.scalars().first()

    async def get_role_by_name(self, db: AsyncSession, name: str) -> Optional[Role]:
        query = select(Role).where(Role.name == name)
        result = await db.execute(query)
        return result.scalars().first()

    async def get_users_list(self, db: AsyncSession, *, skip: int = 0, limit: int = 100) -> List[User]:
        query = select(User).where(User.deleted_at == None).options(
            selectinload(User.role)
        ).offset(skip).limit(limit)
        result = await db.execute(query)
        return list(result.scalars().all())

    async def count_users(self, db: AsyncSession) -> int:
        from sqlalchemy import func
        query = select(func.count()).select_from(User).where(User.deleted_at == None)
        result = await db.execute(query)
        return result.scalar() or 0

user_repository = UserRepository()

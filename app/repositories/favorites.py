import uuid
from typing import List, Optional
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.favorites import Favorite
from app.models.properties import Property
from app.models.locations import City, State
from app.models.users import User
from app.shared.base_repository import BaseRepository

class FavoriteRepository(BaseRepository[Favorite]):
    def __init__(self) -> None:
        super().__init__(Favorite)

    async def get_favorite(self, db: AsyncSession, user_id: uuid.UUID, property_id: uuid.UUID) -> Optional[Favorite]:
        query = select(Favorite).where(
            Favorite.user_id == user_id,
            Favorite.property_id == property_id
        )
        result = await db.execute(query)
        return result.scalars().first()

    async def is_favorite(self, db: AsyncSession, user_id: uuid.UUID, property_id: uuid.UUID) -> bool:
        fav = await self.get_favorite(db, user_id, property_id)
        return fav is not None

    async def get_user_favorites(
        self, db: AsyncSession, user_id: uuid.UUID, skip: int = 0, limit: int = 20
    ) -> List[Favorite]:
        query = (
            select(Favorite)
            .where(Favorite.user_id == user_id)
            .options(
                selectinload(Favorite.property).options(
                    selectinload(Property.city).selectinload(City.state),
                    selectinload(Property.property_type),
                    selectinload(Property.owner).selectinload(User.role),
                    selectinload(Property.images)
                )
            )
            .order_by(Favorite.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        favs = list(result.scalars().all())
        for fav in favs:
            if fav.property:
                fav.property.amenities = []
        return favs

    async def count_user_favorites(self, db: AsyncSession, user_id: uuid.UUID) -> int:
        query = select(func.count()).select_from(Favorite).where(Favorite.user_id == user_id)
        result = await db.execute(query)
        return result.scalar() or 0

favorite_repository = FavoriteRepository()

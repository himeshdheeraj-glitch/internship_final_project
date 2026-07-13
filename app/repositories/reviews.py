import uuid
from typing import List, Optional
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.reviews import Review
from app.shared.base_repository import BaseRepository

class ReviewRepository(BaseRepository[Review]):
    def __init__(self) -> None:
        super().__init__(Review)

    async def get_property_reviews(
        self, db: AsyncSession, property_id: uuid.UUID, skip: int = 0, limit: int = 20
    ) -> List[Review]:
        query = (
            select(Review)
            .where(Review.property_id == property_id, Review.deleted_at == None)
            .options(selectinload(Review.user))
            .order_by(Review.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return list(result.scalars().all())

    async def count_reviews_by_property(self, db: AsyncSession, property_id: uuid.UUID) -> int:
        query = select(func.count()).select_from(Review).where(
            Review.property_id == property_id,
            Review.deleted_at == None
        )
        result = await db.execute(query)
        return result.scalar() or 0

    async def get_property_average_rating(self, db: AsyncSession, property_id: uuid.UUID) -> float:
        query = select(func.avg(Review.rating)).where(
            Review.property_id == property_id,
            Review.deleted_at == None
        )
        result = await db.execute(query)
        val = result.scalar()
        return round(float(val), 2) if val is not None else 0.0

    async def get_user_reviews(
        self, db: AsyncSession, user_id: uuid.UUID, skip: int = 0, limit: int = 20
    ) -> List[Review]:
        query = (
            select(Review)
            .where(Review.user_id == user_id, Review.deleted_at == None)
            .options(selectinload(Review.property))
            .order_by(Review.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return list(result.scalars().all())

    async def count_reviews_total(self, db: AsyncSession) -> int:
        query = select(func.count()).select_from(Review).where(Review.deleted_at == None)
        result = await db.execute(query)
        return result.scalar() or 0

review_repository = ReviewRepository()

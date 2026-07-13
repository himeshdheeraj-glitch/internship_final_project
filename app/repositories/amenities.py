from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.amenities import Amenity
from app.shared.base_repository import BaseRepository

class AmenityRepository(BaseRepository[Amenity]):
    def __init__(self) -> None:
        super().__init__(Amenity)

    async def get_by_name(self, db: AsyncSession, name: str) -> Optional[Amenity]:
        query = select(Amenity).where(Amenity.name.ilike(name))
        result = await db.execute(query)
        return result.scalars().first()

    async def list_amenities(self, db: AsyncSession) -> List[Amenity]:
        query = select(Amenity).order_by(Amenity.name.asc())
        result = await db.execute(query)
        return list(result.scalars().all())

amenity_repository = AmenityRepository()

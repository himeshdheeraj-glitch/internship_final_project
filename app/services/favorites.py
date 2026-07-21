import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import NotFoundException, ConflictException
from app.shared.pagination import Page, PaginationParams
from app.models.favorites import Favorite
from app.repositories.favorites import favorite_repository
from app.repositories.properties import property_repository
from app.repositories.auth import auth_repository

class FavoriteService:
    async def add_favorite(self, db: AsyncSession, *, property_id: uuid.UUID, user_id: uuid.UUID) -> Favorite:
        prop = await property_repository.get(db, property_id)
        if not prop or prop.deleted_at is not None:
            raise NotFoundException(message="Property listing not found")
        existing = await favorite_repository.get_favorite(db, user_id, property_id)
        if existing:
            raise ConflictException(message="Property is already in favorites")
            
        fav = await favorite_repository.create(db, obj_in={"user_id": user_id, "property_id": property_id})
        await auth_repository.create_audit_log(db, user_id=user_id, action="add_favorite", table_name="favorites", record_id=fav.id)
        return await favorite_repository.get_favorite_with_property(db, user_id, property_id)

    async def remove_favorite(self, db: AsyncSession, *, property_id: uuid.UUID, user_id: uuid.UUID) -> None:
        fav = await favorite_repository.get_favorite(db, user_id, property_id)
        if not fav:
            raise NotFoundException(message="Property is not in your favorites list")
        await favorite_repository.remove(db, id=fav.id)
        await auth_repository.create_audit_log(db, user_id=user_id, action="remove_favorite", table_name="favorites", record_id=fav.id)

    async def get_user_favorites(self, db: AsyncSession, *, user_id: uuid.UUID, params: PaginationParams) -> Page:
        skip = (params.page - 1) * params.size
        items = await favorite_repository.get_user_favorites(db, user_id=user_id, skip=skip, limit=params.size)
        total = await favorite_repository.count_user_favorites(db, user_id=user_id)
        return Page.create(items=items, total=total, params=params)

favorite_service = FavoriteService()

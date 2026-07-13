import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.shared.responses import APIResponse
from app.shared.pagination import Page, PaginationParams
from app.core.dependencies import get_current_user
from app.models.users import User
from app.schemas.favorites import FavoriteResponse
from app.services.favorites import favorite_service

router = APIRouter(prefix="/favorites", tags=["Favorites"])

@router.get("", response_model=APIResponse[Page[FavoriteResponse]])
async def get_my_favorites(params: PaginationParams = Depends(), current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    pages = await favorite_service.get_user_favorites(db, user_id=current_user.id, params=params)
    return APIResponse(message="Favorites retrieved", data=pages)

@router.post("/{property_id}", response_model=APIResponse[FavoriteResponse], status_code=status.HTTP_201_CREATED)
async def add_to_favorites(property_id: uuid.UUID, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    fav = await favorite_service.add_favorite(db, property_id=property_id, user_id=current_user.id)
    return APIResponse(message="Property added to favorites", data=fav)

@router.delete("/{property_id}", response_model=APIResponse[None])
async def remove_from_favorites(property_id: uuid.UUID, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    await favorite_service.remove_favorite(db, property_id=property_id, user_id=current_user.id)
    return APIResponse(message="Property removed from favorites")

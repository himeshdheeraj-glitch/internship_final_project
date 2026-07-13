from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.shared.responses import APIResponse
from app.core.permissions import RoleChecker
from app.core.constants import UserRole
from app.core.exceptions import ConflictException
from app.models.users import User
from app.repositories.amenities import amenity_repository
from app.repositories.auth import auth_repository
from app.schemas.amenities import AmenityCreate, AmenityResponse

router = APIRouter(prefix="/amenities", tags=["Amenities"])

@router.get("", response_model=APIResponse[List[AmenityResponse]])
async def get_amenities(db: AsyncSession = Depends(get_db)):
    items = await amenity_repository.list_amenities(db)
    return APIResponse(message="Amenities list retrieved", data=items)

@router.post("", response_model=APIResponse[AmenityResponse], status_code=status.HTTP_201_CREATED)
async def create_amenity(amenity_in: AmenityCreate, current_user: User = Depends(RoleChecker([UserRole.ADMIN])), db: AsyncSession = Depends(get_db)):
    existing = await amenity_repository.get_by_name(db, name=amenity_in.name)
    if existing:
        raise ConflictException(message="Amenity already exists")
    amenity = await amenity_repository.create(db, obj_in=amenity_in.model_dump())
    await auth_repository.create_audit_log(db, user_id=current_user.id, action="create_amenity", table_name="amenities", record_id=amenity.id)
    return APIResponse(message="Amenity created successfully", data=amenity)

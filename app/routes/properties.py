import uuid
from typing import List,Optional
from fastapi import APIRouter, Depends, Query, UploadFile, File, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.shared.responses import APIResponse
from app.shared.pagination import Page, PaginationParams
from app.core.permissions import RoleChecker
from app.core.constants import UserRole
from app.core.dependencies import get_current_user
from app.models.users import User
from app.schemas.properties import PropertyCreate, PropertyUpdate, PropertyResponse, PropertyTypeCreate, PropertyTypeResponse, PropertyImageResponse
from app.services.properties import property_service, image_service

router = APIRouter(tags=["Properties"])

@router.post("/properties", response_model=APIResponse[PropertyResponse], status_code=status.HTTP_201_CREATED)
async def create_property(
    property_in: PropertyCreate,
    current_user: User = Depends(RoleChecker([UserRole.AGENT, UserRole.SELLER, UserRole.ADMIN])),
    db: AsyncSession = Depends(get_db)
):
    prop = await property_service.create_property(db, property_in=property_in, owner_id=current_user.id)
    return APIResponse(message="Property listing created successfully", data=prop)

@router.get("/properties", response_model=APIResponse[Page[PropertyResponse]])
async def list_properties(
    status: Optional[str] = Query("published"),
    city_id: Optional[uuid.UUID] = Query(None),
    property_type_id: Optional[uuid.UUID] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    bedrooms: Optional[int] = Query(None),
    bathrooms: Optional[int] = Query(None),
    min_area: Optional[float] = Query(None),
    max_area: Optional[float] = Query(None),
    is_featured: Optional[bool] = Query(None),
    search_query: Optional[str] = Query(None),
    purpose: Optional[str] = Query(None),
    parking: Optional[bool] = Query(None),
    furnishing_status: Optional[str] = Query(None),
    sort_by: str = Query("created_at_desc"),
    params: PaginationParams = Depends(),
    db: AsyncSession = Depends(get_db)
):
    db_status = None if status == "all" else status
    pages = await property_service.list_properties(
        db, status=db_status, city_id=city_id, property_type_id=property_type_id, min_price=min_price, max_price=max_price,
        bedrooms=bedrooms, bathrooms=bathrooms, min_area=min_area, max_area=max_area, is_featured=is_featured,
        search_query=search_query, purpose=purpose, parking=parking, furnishing_status=furnishing_status,
        sort_by=sort_by, params=params
    )
    return APIResponse(message="Properties list retrieved", data=pages)

@router.get("/properties/{property_id}", response_model=APIResponse[PropertyResponse])
async def get_property_details(property_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    prop = await property_service.get_property(db, property_id=property_id)
    return APIResponse(message="Property details retrieved", data=prop)

@router.put("/properties/{property_id}", response_model=APIResponse[PropertyResponse])
async def update_property_details(
    property_id: uuid.UUID,
    property_update: PropertyUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    is_admin = current_user.role.name == UserRole.ADMIN.value
    prop = await property_service.update_property(db, property_id=property_id, property_update=property_update, user_id=current_user.id, is_admin=is_admin)
    return APIResponse(message="Property updated successfully", data=prop)

@router.delete("/properties/{property_id}", response_model=APIResponse[None])
async def delete_property_listing(property_id: uuid.UUID, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    is_admin = current_user.role.name == UserRole.ADMIN.value
    await property_service.delete_property(db, property_id=property_id, user_id=current_user.id, is_admin=is_admin)
    return APIResponse(message="Property listing deleted successfully")

# Images
@router.post("/properties/{property_id}/images", response_model=APIResponse[PropertyImageResponse], status_code=status.HTTP_201_CREATED)
async def upload_image(property_id: uuid.UUID, file: UploadFile = File(...), current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    is_admin = current_user.role.name == "admin"
    db_image = await image_service.upload_property_image(db, property_id=property_id, file=file, user_id=current_user.id, is_admin=is_admin)
    return APIResponse(message="Image uploaded successfully", data=db_image)

@router.delete("/properties/images/{image_id}", response_model=APIResponse[None])
async def delete_image(image_id: uuid.UUID, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    is_admin = current_user.role.name == "admin"
    await image_service.delete_property_image(db, image_id=image_id, user_id=current_user.id, is_admin=is_admin)
    return APIResponse(message="Image deleted successfully")

@router.post("/properties/{property_id}/images/{image_id}/set-cover", response_model=APIResponse[None])
async def set_cover(property_id: uuid.UUID, image_id: uuid.UUID, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    is_admin = current_user.role.name == "admin"
    await image_service.set_property_cover_image(db, property_id=property_id, image_id=image_id, user_id=current_user.id, is_admin=is_admin)
    return APIResponse(message="Cover image set successfully")

# Types
@router.get("/property-types", response_model=APIResponse[List[PropertyTypeResponse]])
async def get_types(db: AsyncSession = Depends(get_db)):
    types = await property_service.get_property_types(db)
    return APIResponse(message="Property types list retrieved", data=types)

@router.post("/property-types", response_model=APIResponse[PropertyTypeResponse], status_code=status.HTTP_201_CREATED)
async def create_type(type_in: PropertyTypeCreate, current_user: User = Depends(RoleChecker([UserRole.ADMIN])), db: AsyncSession = Depends(get_db)):
    p_type = await property_service.create_property_type(db, name=type_in.name, description=type_in.description, admin_id=current_user.id)
    return APIResponse(message="Property type created successfully", data=p_type)

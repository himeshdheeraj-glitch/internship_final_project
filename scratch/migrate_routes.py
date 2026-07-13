import os

def migrate_routes():
    def write_file(path, content):
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Written: {path}")

    # ==================== app/auth/routes.py ====================
    auth_routes = """from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.shared.responses import APIResponse
from app.core.dependencies import get_current_user
from app.models.users import User
from app.schemas.auth import (
    UserRegister,
    UserLogin,
    TokenResponse,
    RefreshTokenRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest
)
from app.schemas.users import UserResponse
from app.services.auth import auth_service

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=APIResponse[UserResponse], status_code=status.HTTP_201_CREATED)
async def register(user_in: UserRegister, db: AsyncSession = Depends(get_db)):
    user = await auth_service.register_user(db, user_in=user_in)
    return APIResponse(message="User registered successfully", data=user)

@router.post("/login", response_model=APIResponse[TokenResponse], status_code=status.HTTP_200_OK)
async def login(request: Request, credentials: UserLogin, db: AsyncSession = Depends(get_db)):
    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")
    _, tokens = await auth_service.authenticate_user(db, email=credentials.email, password=credentials.password, ip_address=ip_address, user_agent=user_agent)
    return APIResponse(message="Authentication successful", data=tokens)

@router.post("/refresh", response_model=APIResponse[TokenResponse], status_code=status.HTTP_200_OK)
async def refresh(refresh_in: RefreshTokenRequest, db: AsyncSession = Depends(get_db)):
    tokens = await auth_service.refresh_access_token(db, refresh_token=refresh_in.refresh_token)
    return APIResponse(message="Access token refreshed", data=tokens)

@router.post("/logout", response_model=APIResponse[None], status_code=status.HTTP_200_OK)
async def logout(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    await auth_service.logout_user(db, user_id=current_user.id)
    return APIResponse(message="User logged out successfully")

@router.post("/forgot-password", response_model=APIResponse[None], status_code=status.HTTP_200_OK)
async def forgot_password(req: ForgotPasswordRequest):
    return APIResponse(message="Password reset link sent")

@router.post("/reset-password", response_model=APIResponse[None], status_code=status.HTTP_200_OK)
async def reset_password(req: ResetPasswordRequest):
    return APIResponse(message="Password reset successfully")
"""
    write_file("app/auth/routes.py", auth_routes)

    # ==================== app/users/routes.py ====================
    users_routes = """from fastapi import APIRouter, Depends, UploadFile, File, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.shared.responses import APIResponse
from app.core.dependencies import get_current_user
from app.models.users import User
from app.schemas.users import UserResponse, UserUpdate, ChangePasswordRequest
from app.services.users import user_service
from app.shared.file_upload import save_uploaded_file

router = APIRouter(prefix="/users", tags=["Users Profile"])

@router.get("/me", response_model=APIResponse[UserResponse])
async def get_me(current_user: User = Depends(get_current_user)):
    return APIResponse(message="Profile retrieved", data=current_user)

@router.put("/me", response_model=APIResponse[UserResponse])
async def update_me(user_update: UserUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    user = await user_service.update_profile(db, user_id=current_user.id, user_update=user_update)
    return APIResponse(message="Profile updated", data=user)

@router.post("/me/change-password", response_model=APIResponse[None])
async def change_password(req: ChangePasswordRequest, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    await user_service.change_password(db, user_id=current_user.id, old_password=req.old_password, new_password=req.new_password)
    return APIResponse(message="Password changed successfully")

@router.post("/me/profile-image", response_model=APIResponse[UserResponse])
async def upload_profile_image(file: UploadFile = File(...), current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    image_url = await save_uploaded_file(file, folder="profile_images")
    user = await user_service.update_profile(db, user_id=current_user.id, user_update=UserUpdate(profile_image_url=image_url))
    return APIResponse(message="Image uploaded successfully", data=user)
"""
    write_file("app/users/routes.py", users_routes)

    # ==================== app/properties/routes.py ====================
    properties_routes = """import uuid
from typing import Optional
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
    sort_by: str = Query("created_at_desc"),
    params: PaginationParams = Depends(),
    db: AsyncSession = Depends(get_db)
):
    pages = await property_service.list_properties(
        db, status="published", city_id=city_id, property_type_id=property_type_id, min_price=min_price, max_price=max_price,
        bedrooms=bedrooms, bathrooms=bathrooms, min_area=min_area, max_area=max_area, is_featured=is_featured,
        search_query=search_query, sort_by=sort_by, params=params
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
"""
    write_file("app/properties/routes.py", properties_routes)

    # ==================== app/amenities/routes.py ====================
    amenities_routes = """from typing import List
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
"""
    write_file("app/amenities/routes.py", amenities_routes)

    # ==================== app/favorites/routes.py ====================
    favorites_routes = """import uuid
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
"""
    write_file("app/favorites/routes.py", favorites_routes)

    # ==================== app/reviews/routes.py ====================
    reviews_routes = """import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.shared.responses import APIResponse
from app.shared.pagination import Page, PaginationParams
from app.core.dependencies import get_current_user
from app.models.users import User
from app.schemas.reviews import ReviewCreate, ReviewUpdate, ReviewResponse
from app.services.reviews import review_service

router = APIRouter(tags=["Reviews"])

@router.get("/properties/{property_id}/reviews", response_model=APIResponse[Page[ReviewResponse]])
async def get_reviews(property_id: uuid.UUID, params: PaginationParams = Depends(), db: AsyncSession = Depends(get_db)):
    pages = await review_service.get_property_reviews(db, property_id=property_id, params=params)
    return APIResponse(message="Reviews list retrieved", data=pages)

@router.post("/reviews", response_model=APIResponse[ReviewResponse], status_code=status.HTTP_201_CREATED)
async def create_review(review_in: ReviewCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    rev = await review_service.add_review(db, review_in=review_in, user_id=current_user.id)
    return APIResponse(message="Review submitted successfully", data=rev)

@router.put("/reviews/{review_id}", response_model=APIResponse[ReviewResponse])
async def update_review(review_id: uuid.UUID, review_update: ReviewUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    is_admin = current_user.role.name == "admin"
    rev = await review_service.update_review(db, review_id=review_id, review_update=review_update, user_id=current_user.id, is_admin=is_admin)
    return APIResponse(message="Review updated successfully", data=rev)

@router.delete("/reviews/{review_id}", response_model=APIResponse[None])
async def delete_review(review_id: uuid.UUID, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    is_admin = current_user.role.name == "admin"
    await review_service.delete_review(db, review_id=review_id, user_id=current_user.id, is_admin=is_admin)
    return APIResponse(message="Review deleted successfully")
"""
    write_file("app/reviews/routes.py", reviews_routes)

    # ==================== app/locations/routes.py ====================
    locations_routes = """import uuid
from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.shared.responses import APIResponse
from app.core.permissions import RoleChecker
from app.core.constants import UserRole
from app.core.exceptions import ConflictException
from app.models.users import User
from app.repositories.locations import location_repository
from app.schemas.locations import (
    CountryCreate, CountryResponse,
    StateCreate, StateResponse,
    CityCreate, CityResponse
)

router = APIRouter(prefix="/locations", tags=["Locations"])

@router.get("/countries", response_model=APIResponse[List[CountryResponse]])
async def get_countries(db: AsyncSession = Depends(get_db)):
    items = await location_repository.list_countries(db)
    return APIResponse(message="Countries list retrieved", data=items)

@router.post("/countries", response_model=APIResponse[CountryResponse], status_code=status.HTTP_201_CREATED)
async def create_country(country_in: CountryCreate, current_user: User = Depends(RoleChecker([UserRole.ADMIN])), db: AsyncSession = Depends(get_db)):
    existing = await location_repository.get_country_by_code(db, code=country_in.code)
    if existing:
        raise ConflictException(message="Country code already registered")
    country = await location_repository.create_country(db, name=country_in.name, code=country_in.code)
    return APIResponse(message="Country created successfully", data=country)

@router.get("/countries/{country_id}/states", response_model=APIResponse[List[StateResponse]])
async def get_states(country_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    items = await location_repository.list_states_by_country(db, country_id=country_id)
    return APIResponse(message="States list retrieved", data=items)

@router.post("/states", response_model=APIResponse[StateResponse], status_code=status.HTTP_201_CREATED)
async def create_state(state_in: StateCreate, current_user: User = Depends(RoleChecker([UserRole.ADMIN])), db: AsyncSession = Depends(get_db)):
    country = await location_repository.get_country_by_id(db, state_in.country_id)
    if not country:
        raise ConflictException(message="Target country does not exist")
    existing = await location_repository.get_state_by_name_and_country(db, name=state_in.name, country_id=state_in.country_id)
    if existing:
        raise ConflictException(message="State already registered")
    state = await location_repository.create_state(db, name=state_in.name, country_id=state_in.country_id)
    return APIResponse(message="State created successfully", data=state)

@router.get("/states/{state_id}/cities", response_model=APIResponse[List[CityResponse]])
async def get_cities(state_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    items = await location_repository.list_cities_by_state(db, state_id=state_id)
    return APIResponse(message="Cities list retrieved", data=items)

@router.post("/cities", response_model=APIResponse[CityResponse], status_code=status.HTTP_201_CREATED)
async def create_city(city_in: CityCreate, current_user: User = Depends(RoleChecker([UserRole.ADMIN])), db: AsyncSession = Depends(get_db)):
    state = await location_repository.get_state_by_id(db, city_in.state_id)
    if not state:
        raise ConflictException(message="Target state does not exist")
    existing = await location_repository.get_city_by_name_and_state(db, name=city_in.name, state_id=city_in.state_id)
    if existing:
        raise ConflictException(message="City already registered")
    city = await location_repository.create_city(db, name=city_in.name, state_id=city_in.state_id)
    return APIResponse(message="City created successfully", data=city)
"""
    write_file("app/locations/routes.py", locations_routes)

    # ==================== app/notifications/routes.py ====================
    notifications_routes = """import uuid
from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.shared.responses import APIResponse
from app.core.dependencies import get_current_user
from app.models.users import User
from app.schemas.notifications import NotificationResponse
from app.services.notifications import notification_service

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get("", response_model=APIResponse[List[NotificationResponse]])
async def get_my_notifications(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    notifs = await notification_service.get_user_notifications(db, user_id=current_user.id)
    return APIResponse(message="Notifications retrieved", data=notifs)

@router.post("/{notification_id}/read", response_model=APIResponse[NotificationResponse])
async def read_notification(notification_id: uuid.UUID, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    notif = await notification_service.mark_as_read(db, notification_id=notification_id, user_id=current_user.id)
    return APIResponse(message="Notification marked as read", data=notif)

@router.post("/read-all", response_model=APIResponse[None])
async def read_all_notifications(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    await notification_service.mark_all_as_read(db, user_id=current_user.id)
    return APIResponse(message="All notifications marked as read")
"""
    write_file("app/notifications/routes.py", notifications_routes)

    # ==================== app/admin/routes.py ====================
    admin_routes = """import uuid
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.shared.responses import APIResponse
from app.shared.pagination import Page, PaginationParams
from app.core.permissions import RoleChecker
from app.core.constants import UserRole
from app.models.users import User
from app.schemas.users import UserResponse, UserUpdateRole
from app.schemas.properties import PropertyResponse
from app.services.users import user_service
from app.services.properties import property_service
from app.services.analytics import analytics_service

router = APIRouter(prefix="/admin", tags=["Admin Portal"])

@router.get("/users", response_model=APIResponse[List[UserResponse]], dependencies=[Depends(RoleChecker([UserRole.ADMIN]))])
async def list_platform_users(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=100), db: AsyncSession = Depends(get_db)):
    users = await user_service.list_users(db, skip=skip, limit=limit)
    return APIResponse(message="Users list retrieved", data=users)

@router.put("/users/{user_id}/role", response_model=APIResponse[UserResponse])
async def change_user_role(
    user_id: uuid.UUID, role_update: UserUpdateRole, current_admin: User = Depends(RoleChecker([UserRole.ADMIN])), db: AsyncSession = Depends(get_db)
):
    user = await user_service.update_user_role(db, user_id=user_id, role_name=role_update.role_name, admin_id=current_admin.id)
    return APIResponse(message="User role updated successfully", data=user)

@router.post("/users/{user_id}/deactivate", response_model=APIResponse[None])
async def deactivate_user(user_id: uuid.UUID, current_admin: User = Depends(RoleChecker([UserRole.ADMIN])), db: AsyncSession = Depends(get_db)):
    await user_service.deactivate_user(db, user_id=user_id, admin_id=current_admin.id)
    return APIResponse(message="User deactivated successfully")

@router.delete("/users/{user_id}", response_model=APIResponse[None])
async def delete_user(user_id: uuid.UUID, current_admin: User = Depends(RoleChecker([UserRole.ADMIN])), db: AsyncSession = Depends(get_db)):
    await user_service.delete_user(db, user_id=user_id, admin_id=current_admin.id)
    return APIResponse(message="User deleted successfully")

@router.get("/properties", response_model=APIResponse[Page[PropertyResponse]], dependencies=[Depends(RoleChecker([UserRole.ADMIN]))])
async def admin_list_properties(params: PaginationParams = Depends(), db: AsyncSession = Depends(get_db)):
    pages = await property_service.list_properties(db, status=None, params=params)
    return APIResponse(message="Admin listings retrieved", data=pages)

@router.put("/properties/{property_id}/status", response_model=APIResponse[PropertyResponse])
async def change_property_status(
    property_id: uuid.UUID, status_val: str = Query(...), current_admin: User = Depends(RoleChecker([UserRole.ADMIN])), db: AsyncSession = Depends(get_db)
):
    from app.schemas.properties import PropertyUpdate
    update_schema = PropertyUpdate(status=status_val)
    prop = await property_service.update_property(db, property_id=property_id, property_update=update_schema, user_id=current_admin.id, is_admin=True)
    return APIResponse(message="Property status updated successfully", data=prop)

@router.get("/analytics/dashboard", response_model=APIResponse[Dict[str, Any]], dependencies=[Depends(RoleChecker([UserRole.ADMIN]))])
async def get_dashboard_metrics(db: AsyncSession = Depends(get_db)):
    metrics = await analytics_service.get_dashboard_stats(db)
    return APIResponse(message="Metrics retrieved successfully", data=metrics)
"""
    write_file("app/admin/routes.py", admin_routes)

    # ==================== app/main.py ====================
    app_main = """import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.core.logging import logger
from app.middleware.auth import AuthStateMiddleware
from app.middleware.request_logger import RequestLoggerMiddleware
from app.middleware.error_handler import register_error_handlers

# Import modular routes
from app.routes.auth import router as auth_router
from app.routes.users import router as users_router
from app.routes.properties import router as properties_router
from app.routes.amenities import router as amenities_router
from app.routes.favorites import router as favorites_router
from app.routes.reviews import router as reviews_router
from app.routes.locations import router as locations_router
from app.routes.notifications import router as notifications_router
from app.routes.admin import router as admin_router

app = FastAPI(
    title=settings.APP_NAME,
    description="Enterprise Real Estate Platform API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(AuthStateMiddleware)
app.add_middleware(RequestLoggerMiddleware)

register_error_handlers(app)

os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
app.mount("/static/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Include routes
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(users_router, prefix=settings.API_V1_STR)
app.include_router(properties_router, prefix=settings.API_V1_STR)
app.include_router(amenities_router, prefix=settings.API_V1_STR)
app.include_router(favorites_router, prefix=settings.API_V1_STR)
app.include_router(reviews_router, prefix=settings.API_V1_STR)
app.include_router(locations_router, prefix=settings.API_V1_STR)
app.include_router(notifications_router, prefix=settings.API_V1_STR)
app.include_router(admin_router, prefix=settings.API_V1_STR)

@app.on_event("startup")
async def startup_event():
    logger.info("Application starting up...")
    from app.database.session import AsyncSessionLocal
    from app.models.users import Role, User
    from app.core.security import hash_password
    from sqlalchemy.future import select

    async with AsyncSessionLocal() as session:
        for r_name in ["admin", "agent", "seller", "buyer"]:
            res = await session.execute(select(Role).where(Role.name == r_name))
            if not res.scalars().first():
                session.add(Role(name=r_name, description=f"{r_name.capitalize()} role"))
        await session.commit()

        if settings.INIT_ADMIN_EMAIL:
            res_admin = await session.execute(select(User).where(User.email == settings.INIT_ADMIN_EMAIL))
            if not res_admin.scalars().first():
                res_role = await session.execute(select(Role).where(Role.name == "admin"))
                admin_role = res_role.scalars().first()
                if admin_role:
                    session.add(User(
                        email=settings.INIT_ADMIN_EMAIL,
                        hashed_password=hash_password(settings.INIT_ADMIN_PASSWORD),
                        first_name="Platform",
                        last_name="Admin",
                        role_id=admin_role.id,
                        is_active=True,
                        is_verified=True
                    ))
                    await session.commit()
"""
    write_file("app/main.py", app_main)

    print("All Routes and App initialization successfully migrated into modular structure.")

if __name__ == "__main__":
    migrate_routes()

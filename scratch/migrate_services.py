import os

def migrate_services():
    def write_file(path, content):
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Written: {path}")

    # ==================== app/auth/services.py ====================
    auth_services = """import uuid
from datetime import datetime, timezone, timedelta
from typing import Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import ConflictException, UnauthorizedException, BadRequestException
from app.core.logging import logger
from app.core.security import hash_password, verify_password
from app.core.jwt import create_access_token, create_refresh_token, decode_token
from app.models.users import User
from app.repositories.users import user_repository
from app.repositories.auth import auth_repository
from app.schemas.auth import UserRegister, TokenResponse

class AuthService:
    async def register_user(self, db: AsyncSession, *, user_in: UserRegister) -> User:
        logger.info(f"Attempting registration for email: {user_in.email}")
        existing_user = await user_repository.get_by_email(db, user_in.email)
        if existing_user:
            raise ConflictException(message="A user with this email address already exists")
            
        role = await user_repository.get_role_by_name(db, user_in.role_name)
        if not role:
            raise BadRequestException(message="Specified role is invalid or does not exist")
            
        hashed_password = hash_password(user_in.password)
        user_dict = {
            "email": user_in.email,
            "hashed_password": hashed_password,
            "first_name": user_in.first_name,
            "last_name": user_in.last_name,
            "phone_number": user_in.phone_number,
            "role_id": role.id,
            "is_active": True,
            "is_verified": False
        }
        user = await user_repository.create(db, obj_in=user_dict)
        
        await auth_repository.create_audit_log(
            db, user_id=user.id, action="register", table_name="users", record_id=user.id
        )
        return user

    async def authenticate_user(
        self, db: AsyncSession, *, email: str, password: str, ip_address: Optional[str] = None, user_agent: Optional[str] = None
    ) -> Tuple[User, TokenResponse]:
        logger.info(f"Authentication attempt for email: {email}")
        user = await user_repository.get_by_email(db, email)
        if not user or not verify_password(password, user.hashed_password):
            raise UnauthorizedException(message="Incorrect email or password")
            
        if not user.is_active:
            raise UnauthorizedException(message="Inactive account")
            
        await auth_repository.revoke_refresh_tokens(db, user.id)
        
        access_token = create_access_token(subject=str(user.id), role=user.role.name)
        refresh_token_jwt = create_refresh_token(subject=str(user.id))
        
        expiry_dt = datetime.now(timezone.utc) + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
        await auth_repository.create_refresh_token(db, user_id=user.id, token=refresh_token_jwt, expires_at=expiry_dt)
        
        await auth_repository.create_audit_log(
            db, user_id=user.id, action="login", table_name="users", record_id=user.id, ip_address=ip_address, user_agent=user_agent
        )
        return user, TokenResponse(access_token=access_token, refresh_token=refresh_token_jwt)

    async def refresh_access_token(self, db: AsyncSession, *, refresh_token: str) -> TokenResponse:
        payload = decode_token(refresh_token, is_refresh=True)
        user_id_str = payload.get("sub")
        if not user_id_str:
            raise UnauthorizedException(message="Invalid token structure")
            
        db_token = await auth_repository.get_refresh_token(db, refresh_token)
        if not db_token or db_token.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
            raise UnauthorizedException(message="Expired or revoked refresh token")
            
        user = db_token.user
        if not user.is_active:
            raise UnauthorizedException(message="User account is deactivated")
            
        await auth_repository.revoke_refresh_tokens(db, user.id)
        
        new_access_token = create_access_token(subject=str(user.id), role=user.role.name)
        new_refresh_token = create_refresh_token(subject=str(user.id))
        
        expiry_dt = datetime.now(timezone.utc) + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
        await auth_repository.create_refresh_token(db, user_id=user.id, token=new_refresh_token, expires_at=expiry_dt)
        return TokenResponse(access_token=new_access_token, refresh_token=new_refresh_token)

    async def logout_user(self, db: AsyncSession, *, user_id: uuid.UUID) -> None:
        await auth_repository.revoke_refresh_tokens(db, user_id)
        await auth_repository.create_audit_log(db, user_id=user_id, action="logout", table_name="users", record_id=user_id)

auth_service = AuthService()
"""
    write_file("app/auth/services.py", auth_services)

    # ==================== app/users/services.py ====================
    users_services = """import uuid
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundException, BadRequestException
from app.core.logging import logger
from app.core.security import verify_password, hash_password
from app.models.users import User
from app.repositories.users import user_repository
from app.repositories.auth import auth_repository
from app.schemas.users import UserUpdate

class UserService:
    async def get_user_profile(self, db: AsyncSession, *, user_id: uuid.UUID) -> User:
        user = await user_repository.get_user_with_role(db, user_id)
        if not user:
            raise NotFoundException(message="User profile not found")
        return user

    async def update_profile(self, db: AsyncSession, *, user_id: uuid.UUID, user_update: UserUpdate) -> User:
        user = await user_repository.get(db, user_id)
        if not user:
            raise NotFoundException(message="User not found")
        old_values = {"first_name": user.first_name, "last_name": user.last_name, "phone_number": user.phone_number, "profile_image_url": user.profile_image_url}
        await user_repository.update(db, db_obj=user, obj_in=user_update)
        new_values = user_update.model_dump(exclude_unset=True)
        
        await auth_repository.create_audit_log(
            db, user_id=user_id, action="update_profile", table_name="users", record_id=user_id, old_values=old_values, new_values=new_values
        )
        return await user_repository.get_user_with_role(db, user_id)

    async def change_password(self, db: AsyncSession, *, user_id: uuid.UUID, old_password: str, new_password: str) -> None:
        user = await user_repository.get(db, user_id)
        if not user:
            raise NotFoundException(message="User not found")
        if not verify_password(old_password, user.hashed_password):
            raise BadRequestException(message="Incorrect old password")
        new_hashed = hash_password(new_password)
        await user_repository.update(db, db_obj=user, obj_in={"hashed_password": new_hashed})
        await auth_repository.create_audit_log(db, user_id=user_id, action="change_password", table_name="users", record_id=user_id)

    async def update_user_role(self, db: AsyncSession, *, user_id: uuid.UUID, role_name: str, admin_id: uuid.UUID) -> User:
        user = await user_repository.get(db, user_id)
        if not user:
            raise NotFoundException(message="User not found")
        role = await user_repository.get_role_by_name(db, role_name)
        if not role:
            raise BadRequestException(message="Role not found")
            
        old_role_name = user.role.name if user.role else None
        await user_repository.update(db, db_obj=user, obj_in={"role_id": role.id})
        
        await auth_repository.create_audit_log(
            db, user_id=admin_id, action="update_user_role", table_name="users", record_id=user_id, old_values={"role": old_role_name}, new_values={"role": role_name}
        )
        return await user_repository.get_user_with_role(db, user_id)

    async def list_users(self, db: AsyncSession, *, skip: int = 0, limit: int = 100) -> List[User]:
        return await user_repository.get_users_list(db, skip=skip, limit=limit)

    async def deactivate_user(self, db: AsyncSession, *, user_id: uuid.UUID, admin_id: uuid.UUID) -> None:
        user = await user_repository.get(db, user_id)
        if not user:
            raise NotFoundException(message="User not found")
        await user_repository.update(db, db_obj=user, obj_in={"is_active": False})
        await auth_repository.create_audit_log(db, user_id=admin_id, action="deactivate_user", table_name="users", record_id=user_id)

    async def delete_user(self, db: AsyncSession, *, user_id: uuid.UUID, admin_id: uuid.UUID) -> None:
        user = await user_repository.get(db, user_id)
        if not user:
            raise NotFoundException(message="User not found")
        await user_repository.soft_delete(db, id=user_id)
        await auth_repository.create_audit_log(db, user_id=admin_id, action="soft_delete_user", table_name="users", record_id=user_id)

user_service = UserService()
"""
    write_file("app/users/services.py", users_services)

    # ==================== app/properties/services.py ====================
    properties_services = """import uuid
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundException, ForbiddenException, BadRequestException
from app.core.logging import logger
from app.shared.pagination import Page, PaginationParams
from app.models.properties import Property, PropertyType, PropertyImage
from app.repositories.properties import property_repository
from app.repositories.users import user_repository
from app.repositories.auth import auth_repository
from app.schemas.properties import PropertyCreate, PropertyUpdate
from app.utils.file_upload import save_uploaded_file

class PropertyService:
    async def create_property(self, db: AsyncSession, *, property_in: PropertyCreate, owner_id: uuid.UUID) -> Property:
        from app.repositories.locations import location_repository
        city = await location_repository.get_city_by_id(db, property_in.city_id)
        if not city:
            raise NotFoundException(message="Selected city does not exist")
            
        p_type = await property_repository.get(db, property_in.property_type_id)
        if not p_type:
            raise NotFoundException(message="Selected property type does not exist")

        prop_dict = property_in.model_dump(exclude={"amenity_ids"})
        prop_dict["owner_id"] = owner_id
        prop_dict["views_count"] = 0
        
        prop = await property_repository.create(db, obj_in=prop_dict)
        if property_in.amenity_ids:
            for amenity_id in property_in.amenity_ids:
                await property_repository.add_amenity_to_property(db, prop.id, amenity_id)
                
        await auth_repository.create_audit_log(db, user_id=owner_id, action="create_property", table_name="properties", record_id=prop.id)
        return await property_repository.get_property_detail(db, prop.id)

    async def update_property(
        self, db: AsyncSession, *, property_id: uuid.UUID, property_update: PropertyUpdate, user_id: uuid.UUID, is_admin: bool = False
    ) -> Property:
        prop = await property_repository.get(db, property_id)
        if not prop or prop.deleted_at is not None:
            raise NotFoundException(message="Property not found")
        if not is_admin and prop.owner_id != user_id:
            raise ForbiddenException(message="You do not have permissions to modify this listing")
            
        update_dict = property_update.model_dump(exclude_unset=True, exclude={"amenity_ids"})
        if "city_id" in update_dict:
            from app.repositories.locations import location_repository
            city = await location_repository.get_city_by_id(db, update_dict["city_id"])
            if not city:
                raise NotFoundException(message="Selected city does not exist")
        if "property_type_id" in update_dict:
            p_type = await property_repository.get(db, update_dict["property_type_id"])
            if not p_type:
                raise NotFoundException(message="Selected property type does not exist")
                
        await property_repository.update(db, db_obj=prop, obj_in=update_dict)
        if property_update.amenity_ids is not None:
            await property_repository.clear_property_amenities(db, property_id)
            for amenity_id in property_update.amenity_ids:
                await property_repository.add_amenity_to_property(db, property_id, amenity_id)
                
        await auth_repository.create_audit_log(db, user_id=user_id, action="update_property", table_name="properties", record_id=property_id, new_values=property_update.model_dump(exclude_unset=True))
        return await property_repository.get_property_detail(db, property_id)

    async def delete_property(self, db: AsyncSession, *, property_id: uuid.UUID, user_id: uuid.UUID, is_admin: bool = False) -> None:
        prop = await property_repository.get(db, property_id)
        if not prop or prop.deleted_at is not None:
            raise NotFoundException(message="Property not found")
        if not is_admin and prop.owner_id != user_id:
            raise ForbiddenException(message="You do not have permissions to delete this listing")
        await property_repository.soft_delete(db, id=property_id)
        await auth_repository.create_audit_log(db, user_id=user_id, action="delete_property", table_name="properties", record_id=property_id)

    async def get_property(self, db: AsyncSession, *, property_id: uuid.UUID) -> Property:
        prop = await property_repository.get_property_detail(db, property_id)
        if not prop:
            raise NotFoundException(message="Property not found")
        await property_repository.update(db, db_obj=prop, obj_in={"views_count": prop.views_count + 1})
        return prop

    async def list_properties(
        self,
        db: AsyncSession,
        *,
        status: Optional[str] = "published",
        city_id: Optional[uuid.UUID] = None,
        property_type_id: Optional[uuid.UUID] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        bedrooms: Optional[int] = None,
        bathrooms: Optional[int] = None,
        min_area: Optional[float] = None,
        max_area: Optional[float] = None,
        is_featured: Optional[bool] = None,
        search_query: Optional[str] = None,
        sort_by: str = "created_at_desc",
        params: PaginationParams
    ) -> Page[Property]:
        skip = (params.page - 1) * params.size
        items, total = await property_repository.list_properties(
            db, status=status, city_id=city_id, property_type_id=property_type_id, min_price=min_price, max_price=max_price,
            bedrooms=bedrooms, bathrooms=bathrooms, min_area=min_area, max_area=max_area, is_featured=is_featured,
            search_query=search_query, sort_by=sort_by, skip=skip, limit=params.size
        )
        return Page.create(items=items, total=total, params=params)

    async def get_property_types(self, db: AsyncSession) -> List[PropertyType]:
        return await property_repository.list_property_types(db)

    async def create_property_type(self, db: AsyncSession, *, name: str, description: Optional[str] = None, admin_id: uuid.UUID) -> PropertyType:
        existing = await property_repository.get_property_type_by_name(db, name)
        if existing:
            raise ForbiddenException(message="Property type already exists")
        p_type = await property_repository.create_property_type(db, name=name, description=description)
        await auth_repository.create_audit_log(db, user_id=admin_id, action="create_property_type", table_name="property_types", record_id=p_type.id)
        return p_type

class ImageService:
    async def upload_property_image(
        self, db: AsyncSession, *, property_id: uuid.UUID, file, user_id: uuid.UUID, is_admin: bool = False
    ) -> PropertyImage:
        prop = await property_repository.get(db, property_id)
        if not prop or prop.deleted_at is not None:
            raise NotFoundException(message="Property listing not found")
        if not is_admin and prop.owner_id != user_id:
            raise ForbiddenException(message="You do not have permission to manage this listing's images")
            
        file_url = await save_uploaded_file(file, folder="property_images")
        is_cover = len(prop.images) == 0
        display_order = len(prop.images)
        
        db_image = await property_repository.create_property_image(
            db, property_id=property_id, url=file_url, is_cover=is_cover, display_order=display_order
        )
        await auth_repository.create_audit_log(db, user_id=user_id, action="upload_property_image", table_name="property_images", record_id=db_image.id)
        return db_image

    async def delete_property_image(self, db: AsyncSession, *, image_id: uuid.UUID, user_id: uuid.UUID, is_admin: bool = False) -> None:
        img = await property_repository.get_property_image(db, image_id)
        if not img:
            raise NotFoundException(message="Image not found")
        prop = await property_repository.get(db, img.property_id)
        if not prop:
            raise NotFoundException(message="Property listing not found")
        if not is_admin and prop.owner_id != user_id:
            raise ForbiddenException(message="You do not have permission to delete this image")
            
        await property_repository.delete_property_image(db, image_id)
        await auth_repository.create_audit_log(db, user_id=user_id, action="delete_property_image", table_name="property_images", record_id=image_id)

    async def set_property_cover_image(
        self, db: AsyncSession, *, property_id: uuid.UUID, image_id: uuid.UUID, user_id: uuid.UUID, is_admin: bool = False
    ) -> None:
        prop = await property_repository.get(db, property_id)
        if not prop or prop.deleted_at is not None:
            raise NotFoundException(message="Property listing not found")
        if not is_admin and prop.owner_id != user_id:
            raise ForbiddenException(message="You do not have permission to manage cover images")
        img = await property_repository.get_property_image(db, image_id)
        if not img or img.property_id != property_id:
            raise BadRequestException(message="Image does not belong to this property")
            
        await property_repository.set_cover_image(db, property_id, image_id)
        await auth_repository.create_audit_log(db, user_id=user_id, action="set_property_cover_image", table_name="property_images", record_id=image_id)

property_service = PropertyService()
image_service = ImageService()
"""
    write_file("app/properties/services.py", properties_services)

    # ==================== app/favorites/services.py ====================
    favorites_services = """import uuid
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
        return fav

    async def remove_favorite(self, db: AsyncSession, *, property_id: uuid.UUID, user_id: uuid.UUID) -> None:
        fav = await favorite_repository.get_favorite(db, user_id, property_id)
        if not fav:
            raise NotFoundException(message="Property is not in your favorites list")
        await favorite_repository.remove(db, id=fav.id)
        await auth_repository.create_audit_log(db, user_id=user_id, action="remove_favorite", table_name="favorites", record_id=fav.id)

    async def get_user_favorites(self, db: AsyncSession, *, user_id: uuid.UUID, params: PaginationParams) -> Page[Favorite]:
        skip = (params.page - 1) * params.size
        items = await favorite_repository.get_user_favorites(db, user_id=user_id, skip=skip, limit=params.size)
        total = await favorite_repository.count_user_favorites(db, user_id=user_id)
        return Page.create(items=items, total=total, params=params)

favorite_service = FavoriteService()
"""
    write_file("app/favorites/services.py", favorites_services)

    # ==================== app/reviews/services.py ====================
    reviews_services = """import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import NotFoundException, ForbiddenException, BadRequestException
from app.shared.pagination import Page, PaginationParams
from app.models.reviews import Review
from app.repositories.reviews import review_repository
from app.repositories.properties import property_repository
from app.repositories.auth import auth_repository
from app.schemas.reviews import ReviewCreate, ReviewUpdate

class ReviewService:
    async def add_review(self, db: AsyncSession, *, review_in: ReviewCreate, user_id: uuid.UUID) -> Review:
        prop = await property_repository.get(db, review_in.property_id)
        if not prop or prop.deleted_at is not None:
            raise NotFoundException(message="Property not found")
        if prop.owner_id == user_id:
            raise BadRequestException(message="You cannot write reviews for your own property listings")
            
        review_dict = review_in.model_dump()
        review_dict["user_id"] = user_id
        review = await review_repository.create(db, obj_in=review_dict)
        await auth_repository.create_audit_log(db, user_id=user_id, action="create_review", table_name="reviews", record_id=review.id)
        return review

    async def update_review(
        self, db: AsyncSession, *, review_id: uuid.UUID, review_update: ReviewUpdate, user_id: uuid.UUID, is_admin: bool = False
    ) -> Review:
        rev = await review_repository.get(db, review_id)
        if not rev or rev.deleted_at is not None:
            raise NotFoundException(message="Review not found")
        if not is_admin and rev.user_id != user_id:
            raise ForbiddenException(message="You do not have permission to update this review")
            
        update_data = review_update.model_dump(exclude_unset=True)
        await review_repository.update(db, db_obj=rev, obj_in=update_data)
        await auth_repository.create_audit_log(db, user_id=user_id, action="update_review", table_name="reviews", record_id=review_id, new_values=update_data)
        return rev

    async def delete_review(self, db: AsyncSession, *, review_id: uuid.UUID, user_id: uuid.UUID, is_admin: bool = False) -> None:
        rev = await review_repository.get(db, review_id)
        if not rev or rev.deleted_at is not None:
            raise NotFoundException(message="Review not found")
        if not is_admin and rev.user_id != user_id:
            raise ForbiddenException(message="You do not have permission to delete this review")
        await review_repository.soft_delete(db, id=review_id)
        await auth_repository.create_audit_log(db, user_id=user_id, action="delete_review", table_name="reviews", record_id=review_id)

    async def get_property_reviews(self, db: AsyncSession, *, property_id: uuid.UUID, params: PaginationParams) -> Page[Review]:
        skip = (params.page - 1) * params.size
        items = await review_repository.get_property_reviews(db, property_id=property_id, skip=skip, limit=params.size)
        total = await review_repository.count_reviews_by_property(db, property_id=property_id)
        return Page.create(items=items, total=total, params=params)

    async def get_property_average_rating(self, db: AsyncSession, *, property_id: uuid.UUID) -> float:
        return await review_repository.get_property_average_rating(db, property_id)

review_service = ReviewService()
"""
    write_file("app/reviews/services.py", reviews_services)

    # ==================== app/notifications/services.py ====================
    notifications_services = """import uuid
from typing import List
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import NotFoundException, ForbiddenException
from app.models.notifications import Notification

class NotificationService:
    async def send_notification(
        self, db: AsyncSession, *, user_id: uuid.UUID, title: str, message: str, type: str = "info"
    ) -> Notification:
        db_obj = Notification(user_id=user_id, title=title, message=message, type=type, is_read=False)
        db.add(db_obj)
        await db.flush()
        return db_obj

    async def get_user_notifications(self, db: AsyncSession, *, user_id: uuid.UUID) -> List[Notification]:
        query = select(Notification).where(Notification.user_id == user_id).order_by(Notification.created_at.desc())
        result = await db.execute(query)
        return list(result.scalars().all())

    async def mark_as_read(self, db: AsyncSession, *, notification_id: uuid.UUID, user_id: uuid.UUID) -> Notification:
        query = select(Notification).where(Notification.id == notification_id)
        res = await db.execute(query)
        notif = res.scalars().first()
        if not notif:
            raise NotFoundException(message="Notification not found")
        if notif.user_id != user_id:
            raise ForbiddenException(message="Unauthorized access")
        notif.is_read = True
        db.add(notif)
        await db.flush()
        return notif

    async def mark_all_as_read(self, db: AsyncSession, *, user_id: uuid.UUID) -> None:
        stmt = update(Notification).where(
            Notification.user_id == user_id,
            Notification.is_read == False
        ).values(is_read=True)
        await db.execute(stmt)
        await db.flush()

notification_service = NotificationService()
"""
    write_file("app/notifications/services.py", notifications_services)

    # ==================== app/analytics/services.py ====================
    analytics_services = """from typing import Dict, Any, List
from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.users import User
from app.models.properties import Property
from app.models.reviews import Review
from app.models.locations import City
from app.repositories.users import user_repository
from app.repositories.properties import property_repository
from app.repositories.reviews import review_repository

class AnalyticsService:
    async def get_dashboard_stats(self, db: AsyncSession) -> Dict[str, Any]:
        total_users = await user_repository.count_users(db)
        total_properties = await property_repository.count_properties_total(db)
        total_reviews = await review_repository.count_reviews_total(db)

        most_viewed_query = (
            select(Property)
            .where(Property.deleted_at == None, Property.status == "published")
            .order_by(desc(Property.views_count))
            .limit(5)
        )
        res_viewed = await db.execute(most_viewed_query)
        most_viewed = list(res_viewed.scalars().all())

        popular_cities_query = (
            select(City.name, func.count(Property.id).label("property_count"))
            .join(Property, Property.city_id == City.id)
            .where(Property.deleted_at == None)
            .group_by(City.name)
            .order_by(desc("property_count"))
            .limit(5)
        )
        res_cities = await db.execute(popular_cities_query)
        popular_cities = [{"city": row[0], "count": row[1]} for row in res_cities.all()]

        return {
            "totals": {
                "users": total_users,
                "properties": total_properties,
                "reviews": total_reviews
            },
            "most_viewed_properties": [
                {
                    "id": str(p.id),
                    "title": p.title,
                    "price": float(p.price),
                    "views": p.views_count
                }
                for p in most_viewed
            ],
            "popular_cities": popular_cities
        }

analytics_service = AnalyticsService()
"""
    write_file("app/analytics/services.py", analytics_services)

    print("All Services successfully migrated into modular structure.")

if __name__ == "__main__":
    migrate_services()

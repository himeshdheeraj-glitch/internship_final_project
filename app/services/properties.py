import uuid
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
from app.shared.file_upload import save_uploaded_file

class PropertyService:
    async def create_property(self, db: AsyncSession, *, property_in: PropertyCreate, owner_id: uuid.UUID) -> Property:
        from app.repositories.locations import location_repository
        city = await location_repository.get_city_by_id(db, property_in.city_id)
        if not city:
            raise NotFoundException(message="Selected city does not exist")
            
        p_type = await property_repository.get_property_type_by_id(db, property_in.property_type_id)
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
            p_type = await property_repository.get_property_type_by_id(db, update_dict["property_type_id"])
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
        return await property_repository.get_property_detail(db, property_id)

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
        purpose: Optional[str] = None,
        parking: Optional[bool] = None,
        furnishing_status: Optional[str] = None,
        sort_by: str = "created_at_desc",
        params: PaginationParams
    ) -> Page:
        skip = (params.page - 1) * params.size
        items, total = await property_repository.list_properties(
            db, status=status, city_id=city_id, property_type_id=property_type_id, min_price=min_price, max_price=max_price,
            bedrooms=bedrooms, bathrooms=bathrooms, min_area=min_area, max_area=max_area, is_featured=is_featured,
            search_query=search_query, purpose=purpose, parking=parking, furnishing_status=furnishing_status,
            sort_by=sort_by, skip=skip, limit=params.size
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
        prop = await property_repository.get_property_detail(db, property_id)
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

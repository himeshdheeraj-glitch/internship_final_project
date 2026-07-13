import uuid
from typing import List, Optional, Tuple
from sqlalchemy import select, func, and_, or_, desc, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.properties import Property, PropertyImage, PropertyType
from app.models.amenities import PropertyAmenity, Amenity
from app.models.locations import City, State
from app.models.users import User
from app.shared.base_repository import BaseRepository

class PropertyRepository(BaseRepository[Property]):
    def __init__(self) -> None:
        super().__init__(Property)

    async def get_property_detail(self, db: AsyncSession, property_id: uuid.UUID) -> Optional[Property]:
        query = (
            select(Property)
            .where(Property.id == property_id, Property.deleted_at == None)
            .options(
                selectinload(Property.city).selectinload(City.state).selectinload(State.country),
                selectinload(Property.property_type),
                selectinload(Property.owner).selectinload(User.role),
                selectinload(Property.images),
                selectinload(Property.property_amenities).selectinload(PropertyAmenity.amenity)
            )
        )
        result = await db.execute(query)
        prop = result.scalars().first()
        if prop:
            prop.amenities = [pa.amenity for pa in prop.property_amenities]
        return prop

    async def list_properties(
        self,
        db: AsyncSession,
        *,
        status: Optional[str] = None,
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
        skip: int = 0,
        limit: int = 20
    ) -> Tuple[List[Property], int]:
        conditions = [Property.deleted_at == None]

        if status:
            conditions.append(Property.status == status)
        if city_id:
            conditions.append(Property.city_id == city_id)
        if property_type_id:
            conditions.append(Property.property_type_id == property_type_id)
        if min_price is not None:
            conditions.append(Property.price >= min_price)
        if max_price is not None:
            conditions.append(Property.price <= max_price)
        if bedrooms is not None:
            conditions.append(Property.bedrooms == bedrooms)
        if bathrooms is not None:
            conditions.append(Property.bathrooms == bathrooms)
        if min_area is not None:
            conditions.append(Property.area >= min_area)
        if max_area is not None:
            conditions.append(Property.area <= max_area)
        if is_featured is not None:
            conditions.append(Property.is_featured == is_featured)
        if purpose:
            conditions.append(Property.purpose == purpose)
        if parking is not None:
            conditions.append(Property.parking == parking)
        if furnishing_status:
            conditions.append(Property.furnishing_status == furnishing_status)

        if search_query:
            sq_lower = search_query.lower().strip()
            
            # Map category queries to corresponding PropertyType names
            category_types = []
            if sq_lower == "residential":
                category_types = ["Apartment", "House", "Villa"]
            elif sq_lower == "commercial":
                category_types = ["Office", "Shop", "Commercial Building"]
            elif sq_lower == "industrial":
                category_types = ["Warehouse", "Factory"]
            elif sq_lower == "land":
                category_types = ["Plot/Land", "Farm Land", "Agricultural Land"]
                
            # Map subtype queries to their corresponding PropertyType names
            subtype_map = {
                "houses": ["House", "Villa"],
                "house": ["House"],
                "apartments/flats": ["Apartment"],
                "apartment": ["Apartment"],
                "flat": ["Apartment"],
                "villas": ["Villa"],
                "villa": ["Villa"],
                "condominiums (condos)": ["Apartment"],
                "condo": ["Apartment"],
                "townhouses": ["House"],
                "duplexes and triplexes": ["House"],
                "office buildings": ["Office", "Commercial Building"],
                "office": ["Office"],
                "retail shops": ["Shop"],
                "shop": ["Shop"],
                "shopping malls": ["Commercial Building"],
                "hotels": ["Commercial Building"],
                "restaurants": ["Commercial Building"],
                "warehouses": ["Warehouse"],
                "warehouse": ["Warehouse"],
                "factories": ["Factory"],
                "factory": ["Factory"],
                "manufacturing plants": ["Factory"],
                "distribution centers": ["Warehouse"],
                "residential plots": ["Plot/Land"],
                "commercial plots": ["Plot/Land"],
                "agricultural land": ["Agricultural Land"],
                "farm land": ["Farm Land"],
                "development land": ["Plot/Land"]
            }
            
            mapped_types = category_types
            if sq_lower in subtype_map:
                mapped_types = subtype_map[sq_lower]
                
            or_conditions = []
            
            # If we matched specific property types, include those in OR condition
            if mapped_types:
                or_conditions.append(PropertyType.name.in_(mapped_types))
                
            # Also fallback to general ilike search for title, description, etc.
            search_patterns = [f"%{search_query}%"]
            if sq_lower == "factories":
                search_patterns.append("%factory%")
            elif sq_lower == "warehouses":
                search_patterns.append("%warehouse%")
            elif sq_lower == "agricultural land":
                search_patterns.append("%agricultural%")
                search_patterns.append("%land%")
            elif sq_lower == "apartments/flats":
                search_patterns.append("%apartment%")
                search_patterns.append("%flat%")
            elif sq_lower == "residential plots":
                search_patterns.append("%plot%")
                search_patterns.append("%land%")
            elif sq_lower == "commercial plots":
                search_patterns.append("%plot%")
                search_patterns.append("%commercial%")
            elif sq_lower == "farm land":
                search_patterns.append("%farm%")
                search_patterns.append("%land%")
            elif sq_lower == "development land":
                search_patterns.append("%land%")
                search_patterns.append("%development%")

            for pattern in search_patterns:
                or_conditions.extend([
                    Property.title.ilike(pattern),
                    Property.description.ilike(pattern),
                    Property.address.ilike(pattern),
                    PropertyType.name.ilike(pattern),
                    City.name.ilike(pattern)
                ])
            conditions.append(or_(*or_conditions))

        count_query = select(func.count(Property.id)).select_from(Property)
        if search_query:
            count_query = count_query.join(Property.property_type).join(Property.city)
        count_query = count_query.where(and_(*conditions))

        count_result = await db.execute(count_query)
        total = count_result.scalar() or 0

        query = select(Property)
        if search_query:
            query = query.join(Property.property_type).join(Property.city)
        query = query.where(and_(*conditions)).options(
            selectinload(Property.city).selectinload(City.state).selectinload(State.country),
            selectinload(Property.property_type),
            selectinload(Property.owner).selectinload(User.role),
            selectinload(Property.images),
            selectinload(Property.property_amenities).selectinload(PropertyAmenity.amenity)
        )

        if sort_by == "price_asc":
            query = query.order_by(Property.price.asc())
        elif sort_by == "price_desc":
            query = query.order_by(Property.price.desc())
        elif sort_by == "created_at_asc":
            query = query.order_by(Property.created_at.asc())
        else:
            query = query.order_by(Property.created_at.desc())

        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        items = list(result.scalars().all())

        for item in items:
            item.amenities = [pa.amenity for pa in item.property_amenities]
        return items, total

    async def create_property_image(
        self, db: AsyncSession, *, property_id: uuid.UUID, url: str, is_cover: bool = False, display_order: int = 0
    ) -> PropertyImage:
        if is_cover:
            stmt = update(PropertyImage).where(PropertyImage.property_id == property_id).values(is_cover=False)
            await db.execute(stmt)
        db_obj = PropertyImage(property_id=property_id, url=url, is_cover=is_cover, display_order=display_order)
        db.add(db_obj)
        await db.flush()
        return db_obj

    async def get_property_image(self, db: AsyncSession, image_id: uuid.UUID) -> Optional[PropertyImage]:
        query = select(PropertyImage).where(PropertyImage.id == image_id)
        result = await db.execute(query)
        return result.scalars().first()

    async def delete_property_image(self, db: AsyncSession, image_id: uuid.UUID) -> None:
        img = await self.get_property_image(db, image_id)
        if img:
            await db.delete(img)
            await db.flush()

    async def set_cover_image(self, db: AsyncSession, property_id: uuid.UUID, image_id: uuid.UUID) -> None:
        stmt_reset = update(PropertyImage).where(PropertyImage.property_id == property_id).values(is_cover=False)
        await db.execute(stmt_reset)
        stmt_set = update(PropertyImage).where(PropertyImage.id == image_id).values(is_cover=True)
        await db.execute(stmt_set)
        await db.flush()

    async def add_amenity_to_property(self, db: AsyncSession, property_id: uuid.UUID, amenity_id: uuid.UUID) -> None:
        query = select(PropertyAmenity).where(
            PropertyAmenity.property_id == property_id,
            PropertyAmenity.amenity_id == amenity_id
        )
        existing = (await db.execute(query)).scalars().first()
        if not existing:
            db_obj = PropertyAmenity(property_id=property_id, amenity_id=amenity_id)
            db.add(db_obj)
            await db.flush()

    async def remove_amenity_from_property(self, db: AsyncSession, property_id: uuid.UUID, amenity_id: uuid.UUID) -> None:
        query = select(PropertyAmenity).where(
            PropertyAmenity.property_id == property_id,
            PropertyAmenity.amenity_id == amenity_id
        )
        existing = (await db.execute(query)).scalars().first()
        if existing:
            await db.delete(existing)
            await db.flush()

    async def clear_property_amenities(self, db: AsyncSession, property_id: uuid.UUID) -> None:
        stmt = select(PropertyAmenity).where(PropertyAmenity.property_id == property_id)
        res = (await db.execute(stmt)).scalars().all()
        for assoc in res:
            await db.delete(assoc)
        await db.flush()

    async def get_property_type_by_id(self, db: AsyncSession, property_type_id: uuid.UUID) -> Optional[PropertyType]:
        query = select(PropertyType).where(PropertyType.id == property_type_id)
        result = await db.execute(query)
        return result.scalars().first()

    async def get_property_type_by_name(self, db: AsyncSession, name: str) -> Optional[PropertyType]:
        query = select(PropertyType).where(PropertyType.name.ilike(name))
        result = await db.execute(query)
        return result.scalars().first()

    async def create_property_type(self, db: AsyncSession, name: str, description: Optional[str] = None) -> PropertyType:
        db_obj = PropertyType(name=name, description=description)
        db.add(db_obj)
        await db.flush()
        return db_obj

    async def list_property_types(self, db: AsyncSession) -> List[PropertyType]:
        query = select(PropertyType)
        result = await db.execute(query)
        return list(result.scalars().all())

    async def count_properties_total(self, db: AsyncSession) -> int:
        query = select(func.count()).select_from(Property).where(Property.deleted_at == None)
        result = await db.execute(query)
        return result.scalar() or 0

property_repository = PropertyRepository()

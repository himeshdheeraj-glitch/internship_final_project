import os

def migrate_logic():
    def write_file(path, content):
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Written: {path}")

    # ==================== app/core/dependencies.py ====================
    core_dependencies = """import uuid
from typing import AsyncGenerator
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.database.session import get_db
from app.core.config import settings
from app.core.exceptions import UnauthorizedException
from app.core.jwt import decode_token
from app.models.users import User

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    payload = decode_token(token)
    user_id_str = payload.get("sub")
    if not user_id_str:
        raise UnauthorizedException(message="Token payload is missing subject")
    try:
        user_uuid = uuid.UUID(user_id_str)
    except ValueError:
        raise UnauthorizedException(message="Invalid user identifier inside token")
        
    query = select(User).where(User.id == user_uuid, User.deleted_at == None).options(
        selectinload(User.role)
    )
    result = await db.execute(query)
    user = result.scalars().first()
    
    if not user:
        raise UnauthorizedException(message="User matching credentials does not exist")
    if not user.is_active:
        raise UnauthorizedException(message="User account is deactivated")
    return user

def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise UnauthorizedException(message="Inactive user account")
    return current_user
"""
    write_file("app/core/dependencies.py", core_dependencies)

    # ==================== app/auth/repositories.py ====================
    auth_repos = """import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.auth import RefreshToken, AuditLog
from app.models.users import User

class AuthRepository:
    async def get_refresh_token(self, db: AsyncSession, token: str) -> Optional[RefreshToken]:
        query = select(RefreshToken).where(
            RefreshToken.token == token,
            RefreshToken.is_revoked == False
        ).options(selectinload(RefreshToken.user).selectinload(User.role))
        result = await db.execute(query)
        return result.scalars().first()

    async def create_refresh_token(
        self, db: AsyncSession, *, user_id: uuid.UUID, token: str, expires_at: datetime
    ) -> RefreshToken:
        db_obj = RefreshToken(user_id=user_id, token=token, expires_at=expires_at)
        db.add(db_obj)
        await db.flush()
        return db_obj

    async def revoke_refresh_tokens(self, db: AsyncSession, user_id: uuid.UUID) -> None:
        query = update(RefreshToken).where(
            RefreshToken.user_id == user_id,
            RefreshToken.is_revoked == False
        ).values(is_revoked=True)
        await db.execute(query)
        await db.flush()

    async def create_audit_log(
        self,
        db: AsyncSession,
        *,
        user_id: Optional[uuid.UUID],
        action: str,
        table_name: str,
        record_id: Optional[uuid.UUID] = None,
        old_values: Optional[dict] = None,
        new_values: Optional[dict] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> AuditLog:
        db_obj = AuditLog(
            user_id=user_id,
            action=action,
            table_name=table_name,
            record_id=record_id,
            old_values=old_values,
            new_values=new_values,
            ip_address=ip_address,
            user_agent=user_agent
        )
        db.add(db_obj)
        await db.flush()
        return db_obj

auth_repository = AuthRepository()
"""
    write_file("app/auth/repositories.py", auth_repos)

    # ==================== app/users/repositories.py ====================
    users_repos = """import uuid
from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.users import User, Role
from app.repositories.base_repository import BaseRepository

class UserRepository(BaseRepository[User]):
    def __init__(self) -> None:
        super().__init__(User)

    async def get_by_email(self, db: AsyncSession, email: str) -> Optional[User]:
        query = select(User).where(User.email == email, User.deleted_at == None).options(
            selectinload(User.role)
        )
        result = await db.execute(query)
        return result.scalars().first()

    async def get_user_with_role(self, db: AsyncSession, user_id: uuid.UUID) -> Optional[User]:
        query = select(User).where(User.id == user_id, User.deleted_at == None).options(
            selectinload(User.role)
        )
        result = await db.execute(query)
        return result.scalars().first()

    async def get_role_by_name(self, db: AsyncSession, name: str) -> Optional[Role]:
        query = select(Role).where(Role.name == name)
        result = await db.execute(query)
        return result.scalars().first()

    async def get_users_list(self, db: AsyncSession, *, skip: int = 0, limit: int = 100) -> List[User]:
        query = select(User).where(User.deleted_at == None).options(
            selectinload(User.role)
        ).offset(skip).limit(limit)
        result = await db.execute(query)
        return list(result.scalars().all())

    async def count_users(self, db: AsyncSession) -> int:
        from sqlalchemy import func
        query = select(func.count()).select_from(User).where(User.deleted_at == None)
        result = await db.execute(query)
        return result.scalar() or 0

user_repository = UserRepository()
"""
    write_file("app/users/repositories.py", users_repos)

    # ==================== app/locations/repositories.py ====================
    locations_repos = """import uuid
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.locations import Country, State, City

class LocationRepository:
    async def get_country_by_id(self, db: AsyncSession, country_id: uuid.UUID) -> Optional[Country]:
        query = select(Country).where(Country.id == country_id)
        result = await db.execute(query)
        return result.scalars().first()

    async def get_country_by_name(self, db: AsyncSession, name: str) -> Optional[Country]:
        query = select(Country).where(Country.name.ilike(name))
        result = await db.execute(query)
        return result.scalars().first()

    async def get_country_by_code(self, db: AsyncSession, code: str) -> Optional[Country]:
        query = select(Country).where(Country.code.ilike(code))
        result = await db.execute(query)
        return result.scalars().first()

    async def create_country(self, db: AsyncSession, name: str, code: str) -> Country:
        db_obj = Country(name=name, code=code)
        db.add(db_obj)
        await db.flush()
        return db_obj

    async def list_countries(self, db: AsyncSession) -> List[Country]:
        query = select(Country).order_by(Country.name.asc())
        result = await db.execute(query)
        return list(result.scalars().all())

    async def get_state_by_id(self, db: AsyncSession, state_id: uuid.UUID) -> Optional[State]:
        query = select(State).where(State.id == state_id).options(selectinload(State.country))
        result = await db.execute(query)
        return result.scalars().first()

    async def get_state_by_name_and_country(self, db: AsyncSession, name: str, country_id: uuid.UUID) -> Optional[State]:
        query = select(State).where(State.name.ilike(name), State.country_id == country_id)
        result = await db.execute(query)
        return result.scalars().first()

    async def create_state(self, db: AsyncSession, name: str, country_id: uuid.UUID) -> State:
        db_obj = State(name=name, country_id=country_id)
        db.add(db_obj)
        await db.flush()
        return db_obj

    async def list_states_by_country(self, db: AsyncSession, country_id: uuid.UUID) -> List[State]:
        query = select(State).where(State.country_id == country_id).order_by(State.name.asc())
        result = await db.execute(query)
        return list(result.scalars().all())

    async def get_city_by_id(self, db: AsyncSession, city_id: uuid.UUID) -> Optional[City]:
        query = select(City).where(City.id == city_id).options(selectinload(City.state).selectinload(State.country))
        result = await db.execute(query)
        return result.scalars().first()

    async def get_city_by_name_and_state(self, db: AsyncSession, name: str, state_id: uuid.UUID) -> Optional[City]:
        query = select(City).where(City.name.ilike(name), City.state_id == state_id)
        result = await db.execute(query)
        return result.scalars().first()

    async def create_city(self, db: AsyncSession, name: str, state_id: uuid.UUID) -> City:
        db_obj = City(name=name, state_id=state_id)
        db.add(db_obj)
        await db.flush()
        return db_obj

    async def list_cities_by_state(self, db: AsyncSession, state_id: uuid.UUID) -> List[City]:
        query = select(City).where(City.state_id == state_id).order_by(City.name.asc())
        result = await db.execute(query)
        return list(result.scalars().all())

location_repository = LocationRepository()
"""
    write_file("app/locations/repositories.py", locations_repos)

    # ==================== app/properties/repositories.py ====================
    properties_repos = """import uuid
from typing import List, Optional, Tuple
from sqlalchemy import select, func, and_, or_, desc, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.properties import Property, PropertyImage, PropertyType
from app.models.amenities import PropertyAmenity, Amenity
from app.models.locations import City, State
from app.repositories.base_repository import BaseRepository

class PropertyRepository(BaseRepository[Property]):
    def __init__(self) -> None:
        super().__init__(Property)

    async def get_property_detail(self, db: AsyncSession, property_id: uuid.UUID) -> Optional[Property]:
        query = (
            select(Property)
            .where(Property.id == property_id, Property.deleted_at == None)
            .options(
                selectinload(Property.city).selectinload(City.state),
                selectinload(Property.property_type),
                selectinload(Property.owner),
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

        if search_query:
            search_pattern = f"%{search_query}%"
            conditions.append(
                or_(
                    Property.title.ilike(search_pattern),
                    Property.description.ilike(search_pattern),
                    Property.address.ilike(search_pattern)
                )
            )

        count_query = select(func.count(Property.id)).where(and_(*conditions))
        count_result = await db.execute(count_query)
        total = count_result.scalar() or 0

        query = select(Property).where(and_(*conditions)).options(
            selectinload(Property.city).selectinload(City.state),
            selectinload(Property.property_type),
            selectinload(Property.owner),
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
"""
    write_file("app/properties/repositories.py", properties_repos)

    # ==================== app/amenities/repositories.py ====================
    amenities_repos = """from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.amenities import Amenity
from app.repositories.base_repository import BaseRepository

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
"""
    write_file("app/amenities/repositories.py", amenities_repos)

    # ==================== app/favorites/repositories.py ====================
    favorites_repos = """import uuid
from typing import List, Optional
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.favorites import Favorite
from app.models.properties import Property
from app.models.locations import City, State
from app.repositories.base_repository import BaseRepository

class FavoriteRepository(BaseRepository[Favorite]):
    def __init__(self) -> None:
        super().__init__(Favorite)

    async def get_favorite(self, db: AsyncSession, user_id: uuid.UUID, property_id: uuid.UUID) -> Optional[Favorite]:
        query = select(Favorite).where(
            Favorite.user_id == user_id,
            Favorite.property_id == property_id
        )
        result = await db.execute(query)
        return result.scalars().first()

    async def is_favorite(self, db: AsyncSession, user_id: uuid.UUID, property_id: uuid.UUID) -> bool:
        fav = await self.get_favorite(db, user_id, property_id)
        return fav is not None

    async def get_user_favorites(
        self, db: AsyncSession, user_id: uuid.UUID, skip: int = 0, limit: int = 20
    ) -> List[Favorite]:
        query = (
            select(Favorite)
            .where(Favorite.user_id == user_id)
            .options(
                selectinload(Favorite.property).options(
                    selectinload(Property.city).selectinload(City.state),
                    selectinload(Property.property_type),
                    selectinload(Property.owner),
                    selectinload(Property.images)
                )
            )
            .order_by(Favorite.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        favs = list(result.scalars().all())
        for fav in favs:
            if fav.property:
                fav.property.amenities = []
        return favs

    async def count_user_favorites(self, db: AsyncSession, user_id: uuid.UUID) -> int:
        query = select(func.count()).select_from(Favorite).where(Favorite.user_id == user_id)
        result = await db.execute(query)
        return result.scalar() or 0

favorite_repository = FavoriteRepository()
"""
    write_file("app/favorites/repositories.py", favorites_repos)

    # ==================== app/reviews/repositories.py ====================
    reviews_repos = """import uuid
from typing import List, Optional
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.reviews import Review
from app.repositories.base_repository import BaseRepository

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
"""
    write_file("app/reviews/repositories.py", reviews_repos)

    print("All Repositories successfully migrated into modular structure.")

if __name__ == "__main__":
    migrate_logic()

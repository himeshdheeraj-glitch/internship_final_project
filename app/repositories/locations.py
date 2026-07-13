import uuid
from typing import List, Optional
from sqlalchemy import select, func
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
        query = select(State).where(State.country_id == country_id).options(selectinload(State.country)).order_by(State.name.asc())
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
        query = select(City).where(City.state_id == state_id).options(selectinload(City.state).selectinload(State.country)).order_by(City.name.asc())
        result = await db.execute(query)
        return list(result.scalars().all())

    async def count_locations_total(self, db: AsyncSession) -> int:
        query = select(func.count()).select_from(City)
        result = await db.execute(query)
        return result.scalar() or 0

location_repository = LocationRepository()

import uuid
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
async def create_country(country_in: CountryCreate, current_user: User = Depends(RoleChecker([UserRole.ADMIN, UserRole.AGENT, UserRole.SELLER])), db: AsyncSession = Depends(get_db)):
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
async def create_state(state_in: StateCreate, current_user: User = Depends(RoleChecker([UserRole.ADMIN, UserRole.AGENT, UserRole.SELLER])), db: AsyncSession = Depends(get_db)):
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
async def create_city(city_in: CityCreate, current_user: User = Depends(RoleChecker([UserRole.ADMIN, UserRole.AGENT, UserRole.SELLER])), db: AsyncSession = Depends(get_db)):
    state = await location_repository.get_state_by_id(db, city_in.state_id)
    if not state:
        raise ConflictException(message="Target state does not exist")
    existing = await location_repository.get_city_by_name_and_state(db, name=city_in.name, state_id=city_in.state_id)
    if existing:
        raise ConflictException(message="City already registered")
    city = await location_repository.create_city(db, name=city_in.name, state_id=city_in.state_id)
    return APIResponse(message="City created successfully", data=city)

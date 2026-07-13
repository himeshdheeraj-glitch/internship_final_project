import os
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
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?$",
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

        # Seed Property Types
        from app.models.properties import PropertyType
        for pt_name in ["Apartment", "House", "Villa", "Plot/Land", "Office", "Shop", "Warehouse", "Farm Land", "Commercial Building", "Factory", "Agricultural Land"]:
            res_pt = await session.execute(select(PropertyType).where(PropertyType.name == pt_name))
            if not res_pt.scalars().first():
                session.add(PropertyType(name=pt_name, description=f"{pt_name} property type"))
        await session.commit()

        # Seed Amenities
        from app.models.amenities import Amenity
        for am_name in ["Gym", "Swimming Pool", "Garden", "Security", "Parking", "Internet", "Air Conditioning"]:
            res_am = await session.execute(select(Amenity).where(Amenity.name == am_name))
            if not res_am.scalars().first():
                session.add(Amenity(name=am_name, description=f"{am_name} amenity"))
        await session.commit()

        # Seed Locations
        from app.models.locations import Country, State, City
        res_country = await session.execute(select(Country).where(Country.code == "IN"))
        country = res_country.scalars().first()
        if not country:
            country = Country(name="India", code="IN")
            session.add(country)
            await session.flush()

        indian_locations = {
            "Karnataka": ["Bengaluru", "Mysuru"],
            "Maharashtra": ["Mumbai", "Pune"],
            "Delhi": ["New Delhi"],
            "Telangana": ["Hyderabad"]
        }

        for state_name, cities_list in indian_locations.items():
            res_state = await session.execute(select(State).where(State.name == state_name, State.country_id == country.id))
            state = res_state.scalars().first()
            if not state:
                state = State(name=state_name, country_id=country.id)
                session.add(state)
                await session.flush()

            for city_name in cities_list:
                res_city = await session.execute(select(City).where(City.name == city_name, City.state_id == state.id))
                city = res_city.scalars().first()
                if not city:
                    city = City(name=city_name, state_id=state.id)
                    session.add(city)
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
# Reload trigger comment

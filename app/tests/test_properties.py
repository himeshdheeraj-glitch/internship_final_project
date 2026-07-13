import asyncio
import uuid

from app.database.session import AsyncSessionLocal
from app.models.locations import City, Country, State
from app.models.properties import PropertyType
from app.models.users import Role, User
from app.schemas.properties import PropertyCreate
from app.services.properties import property_service


def test_create_property_accepts_valid_property_type():
    async def run_test() -> None:
        async with AsyncSessionLocal() as db:
            role = Role(name=f"seller-{uuid.uuid4().hex[:8]}", description="seller")
            db.add(role)
            await db.flush()

            user = User(
                email=f"seller-{uuid.uuid4().hex[:8]}@example.com",
                hashed_password="hashed",
                first_name="Test",
                last_name="Seller",
                role_id=role.id,
                is_active=True,
                is_verified=True,
            )
            db.add(user)
            await db.flush()

            country = Country(name=f"Country-{uuid.uuid4().hex[:6]}", code=f"CT{uuid.uuid4().hex[:4]}")
            db.add(country)
            await db.flush()

            state = State(name=f"State-{uuid.uuid4().hex[:6]}", country_id=country.id)
            db.add(state)
            await db.flush()

            city = City(name=f"City-{uuid.uuid4().hex[:6]}", state_id=state.id)
            db.add(city)
            await db.flush()

            property_type = PropertyType(name=f"Type-{uuid.uuid4().hex[:6]}", description="Test property type")
            db.add(property_type)
            await db.flush()

            property_in = PropertyCreate(
                title="Test Property",
                description="A property created during regression testing.",
                price=250000,
                bedrooms=3,
                bathrooms=2,
                area=1800,
                address="123 Test Street",
                zip_code="10001",
                city_id=city.id,
                property_type_id=property_type.id,
                status="published",
                is_featured=False,
                amenity_ids=[],
            )

            created_property = await property_service.create_property(db, property_in=property_in, owner_id=user.id)

            assert created_property.id is not None
            assert created_property.property_type_id == property_type.id
            assert created_property.owner_id == user.id

            await db.rollback()

    asyncio.run(run_test())

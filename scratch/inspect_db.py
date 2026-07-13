import asyncio
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.database.session import AsyncSessionLocal
from app.models.users import User, Role
from app.models.properties import Property, PropertyType
from app.models.locations import City

async def inspect():
    async with AsyncSessionLocal() as session:
        # Roles
        roles_res = await session.execute(select(Role))
        roles = roles_res.scalars().all()
        print("--- ROLES ---")
        for r in roles:
            print(f"Role: ID={r.id}, Name={r.name}")

        # Users
        users_res = await session.execute(select(User).options(selectinload(User.role)))
        users = users_res.scalars().all()
        print("\n--- USERS ---")
        for u in users:
            print(f"User: ID={u.id}, Email={u.email}, Name={u.first_name} {u.last_name}, Role={u.role.name}")

        # Property Types
        pts_res = await session.execute(select(PropertyType))
        pts = pts_res.scalars().all()
        print("\n--- PROPERTY TYPES ---")
        for pt in pts:
            print(f"Type: ID={pt.id}, Name={pt.name}")

        # Properties
        props_res = await session.execute(select(Property).options(selectinload(Property.owner), selectinload(Property.property_type)))
        props = props_res.scalars().all()
        print("\n--- PROPERTIES ---")
        for p in props:
            owner_email = p.owner.email if p.owner else "No Owner"
            type_name = p.property_type.name if p.property_type else "No Type"
            print(f"Property: ID={p.id}, Title={p.title}, Owner={owner_email}, Type={type_name}, Status={p.status}, Price={p.price}")

if __name__ == "__main__":
    asyncio.run(inspect())

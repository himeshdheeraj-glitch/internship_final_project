import asyncio
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.future import select
from app.database.session import AsyncSessionLocal
from app.models.locations import Country, State, City

async def main():
    async with AsyncSessionLocal() as session:
        print("--- Countries ---")
        res = await session.execute(select(Country))
        countries = res.scalars().all()
        for c in countries:
            print(f"Country: {c.name} ({c.code}) - ID: {c.id}")
            
        print("\n--- States ---")
        res = await session.execute(select(State))
        states = res.scalars().all()
        for s in states:
            print(f"State: {s.name} - Country ID: {s.country_id} - ID: {s.id}")
            
        print("\n--- Cities ---")
        res = await session.execute(select(City))
        cities = res.scalars().all()
        for ci in cities:
            print(f"City: {ci.name} - State ID: {ci.state_id} - ID: {ci.id}")

if __name__ == "__main__":
    asyncio.run(main())

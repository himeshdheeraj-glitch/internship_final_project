import asyncio
from sqlalchemy.future import select
from app.database.session import AsyncSessionLocal
from app.models.properties import PropertyImage

async def check():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(PropertyImage))
        images = result.scalars().all()
        print("Total images in DB:", len(images))
        for img in images:
            print(f"ID: {img.id}, Prop ID: {img.property_id}, URL: '{img.url}', Is Cover: {img.is_cover}")

if __name__ == "__main__":
    asyncio.run(check())

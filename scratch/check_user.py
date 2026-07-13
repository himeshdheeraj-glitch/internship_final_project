import asyncio
from app.database.session import AsyncSessionLocal
from app.models.users import User
from sqlalchemy import select

async def main():
    async with AsyncSessionLocal() as db:
        res = await db.execute(select(User).where(User.email.ilike('newuser@example.com')))
        users = res.scalars().all()
        print('users:', users)

asyncio.run(main())

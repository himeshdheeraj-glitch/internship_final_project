import asyncio
from sqlalchemy import inspect
from app.database.session import AsyncSessionLocal

async def inspect_columns():
    async with AsyncSessionLocal() as session:
        conn = await session.connection()
        def get_cols(connection):
            inspector = inspect(connection)
            print("--- COLUMNS IN PROPERTIES ---")
            for col in inspector.get_columns("properties"):
                print(f"Column: {col['name']}, Type: {col['type']}, Nullable: {col['nullable']}")
            
            print("\n--- COLUMNS IN USERS ---")
            for col in inspector.get_columns("users"):
                print(f"Column: {col['name']}, Type: {col['type']}, Nullable: {col['nullable']}")
        
        await conn.run_sync(get_cols)

if __name__ == "__main__":
    asyncio.run(inspect_columns())

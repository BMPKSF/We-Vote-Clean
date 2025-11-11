import asyncio
from app.db.database import engine, Base
import os

print("Current working directory:", os.getcwd())
print("Env file exists:", os.path.exists(".env"))

async def run():
    async with engine.begin() as conn:
        # Create all tables from models
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created successfully!")

if __name__ == "__main__":
    asyncio.run(run())

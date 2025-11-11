import asyncio
from app.db.database import engine

async def test():
    try:
        async with engine.connect() as conn:
            result = await conn.execute("SELECT 1")
            value = result.scalar()
            print("Connection successful! SELECT 1 returned:", value)
    except Exception as e:
        print("Connection failed:", e)
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(test())

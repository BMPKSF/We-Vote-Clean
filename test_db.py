import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()  # load your .env file

DATABASE_URL = os.getenv("DATABASE_URL")

async def test_connection():
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        print("Connection successful!")
        await conn.close()
    except Exception as e:
        print("Connection failed:", e)

asyncio.run(test_connection())

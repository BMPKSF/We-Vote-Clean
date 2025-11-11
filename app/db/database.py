import ssl
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

# Create SSL context for asyncpg (Supabase requires SSL)
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE  # DEV/TEST only; verify in production

# Use the DATABASE_URL from your settings directly
DATABASE_URL = settings.database_url

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True,
    connect_args={"ssl": ssl_context}  # proper SSL object
)

# Async session factory
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

# Base for models
Base = declarative_base()

# FastAPI dependency
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# Optional connect/disconnect helpers
async def connect():
    pass  # noop for async engine

async def disconnect():
    await engine.dispose()

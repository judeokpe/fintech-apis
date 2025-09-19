import os

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@db:5432/postgres")

engine = create_async_engine(DATABASE_URL, future=True, pool_pre_ping=True)

AsyncSessionLocal = sessionmaker(bind = engine, class_ = AsyncSession, expire_on_commit=False)
Base = declarative_base()


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
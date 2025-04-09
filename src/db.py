from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from src.config import settings

Base = declarative_base()
engine = create_async_engine(settings.DATABASE_URL)
session_factory = async_sessionmaker(engine, autoflush=False, autocommit=False)


async def get_session():
    async with session_factory() as session:
        yield session

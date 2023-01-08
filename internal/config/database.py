from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from internal.config.config import config
from internal.entity.base import Base

from typing import Generator

engine = create_async_engine(config.database_url, echo=True)
Base = Base

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_session() -> Generator[scoped_session, None, None]:
    async with async_session() as session:
        yield session
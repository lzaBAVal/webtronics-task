from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from internal.config.config import get_config

from typing import Generator


config = get_config()
engine = create_async_engine(config.db.get_url(), echo=True)

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_session() -> Generator[scoped_session, None, None]:
    async with async_session() as session:
        yield session

#TODO create app start and app finish
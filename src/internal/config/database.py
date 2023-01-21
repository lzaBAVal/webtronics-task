from asyncio import current_task
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_scoped_session
from sqlalchemy.orm import sessionmaker, scoped_session

from internal.config.config import get_config

from typing import Generator


config = get_config()
# print('#'*40, config.db.get_url())
engine = create_async_engine(config.db.get_url(), echo=True)

async_session_factory = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async_scoped_session = async_scoped_session(async_session_factory, scopefunc=current_task)

async def get_session() -> Generator[scoped_session, None, None]:
    async with async_scoped_session() as session:
        yield session

#TODO create app start and app finish
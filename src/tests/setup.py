from asyncio import current_task
from typing import Generator

from fastapi import FastAPI
from fastapi.testclient import TestClient

from internal.config.config import get_config
from internal.config.database import get_session

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_scoped_session
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import NullPool


config = get_config()

engine = create_async_engine(config.db.get_url(), echo=True, poolclass=NullPool)

async_session_factory = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False, autocommit=False, autoflush=False
)

AsyncScopedSession = async_scoped_session(async_session_factory, scopefunc=current_task)


async def get_test_session() -> Generator[scoped_session, None, None]:
    session = AsyncScopedSession()
    await session.begin_nested()
    
    yield session

    await session.rollback()
    # await session.flush()
    await session.close()


def get_test_client(app: FastAPI):
    app.dependency_overrides[get_session] = get_test_session
    return TestClient(app)
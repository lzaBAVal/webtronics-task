from fastapi import FastAPI
from fastapi.testclient import TestClient

from internal.config.config import get_config
from internal.config.database import get_session

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from typing import Generator


config = get_config(
    _env_file="test.env",
    _env_file_encoding = 'utf-8'
)

engine = create_async_engine(config.db.get_url(), echo=True)

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_test_session() -> Generator[scoped_session, None, None]:
    async with async_session() as session:
        yield session


def get_test_client(app: FastAPI):
    app.dependency_overrides[get_session] = get_test_session
    return TestClient(app)
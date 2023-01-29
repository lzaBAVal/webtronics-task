from asyncio import current_task
from typing import Callable, Generator, Type
from fastapi import Depends

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_scoped_session
from sqlalchemy.orm import sessionmaker, Session

from internal.config.config import get_config
from internal.repository.base import BaseRepository


config = get_config()
engine = create_async_engine(config.db.get_url(), echo=True)

async_session_factory = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

AsuncScopedSession = async_scoped_session(async_session_factory, scopefunc=current_task)


async def get_session() -> Generator[async_scoped_session, None, None]:
    async with AsuncScopedSession() as session:
        yield session
        await session.commit()


def get_repository(repo_type: Type[BaseRepository],) -> Callable[[Session], BaseRepository]:
    def _get_repo(session: Session = Depends(get_session)) -> BaseRepository:
        return repo_type(session)

    return _get_repo
    
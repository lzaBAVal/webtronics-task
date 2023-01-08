from typing import List
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from internal.config.database import get_session

from internal.entity.user import User

class UserService(object):
    def __init__(self, session: AsyncSession = Depends(get_session)) -> None:
        self.session = session

    async def get_all(self, limit: int = 10, offset: int = 0) -> List[User]:
        res = await self.session.execute(select(User).limit(limit).offset(offset))
        res = res.scalars().all()
        return res

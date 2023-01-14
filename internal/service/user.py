from typing import List
from fastapi import Depends
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from internal.config.database import get_session
from internal.config.redis import get_redis_session
from internal.dto.user import UpdateUserDTO, UserDTO

from internal.entity.user import User
from internal.exceptions.user import UserNotFoundError
from internal.service.auth import get_current_user


class UserService(object):
    def __init__(
        self, 
        session: AsyncSession = Depends(get_session), 
        redis_session = Depends(get_redis_session),
        user: UserDTO = Depends(get_current_user)
    ) -> None:
        self.session = session
        self.redis_session = redis_session
        self.user = user

    async def get_all(self, limit: int = 10, offset: int = 0) -> List[UserDTO]:
        res = await self.session.execute(select(User).limit(limit).offset(offset))
        return res.scalars().all()

    async def get(self) -> User:
        user = await self.session.execute(select(User).filter_by(id=self.user.id))
        user = user.scalar()

        if user:
            return user
        raise UserNotFoundError(id)

    async def update(self, dto: UpdateUserDTO) -> User:

        await self.session.execute(update(User).filter_by(email=self.user.email).values(**dto.dict()))
        await self.session.commit()

        user = await self.session.execute(select(User).filter_by(email=self.user.email))
        user = user.scalar()
    
        if user:
            return user
        raise UserNotFoundError(id)

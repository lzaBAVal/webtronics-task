from typing import List
from fastapi import Depends
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from internal.config.database import get_session
from internal.dto.user import FullUserDTO, UpdateUserDTO, UserDTO

from internal.entity.user import User
from internal.exceptions.user import UserNotFoundError


class UserService(object):
    def __init__(self, session: AsyncSession = Depends(get_session)) -> None:
        self.session = session

    async def get_all(self, limit: int = 10, offset: int = 0) -> List[UserDTO]:
        res = await self.session.execute(select(User).limit(limit).offset(offset))
        res = res.scalars().all()
        return res

    async def get(self, id: str) -> UserDTO:
        user = await self.session.execute(select(User).filter_by(id=id))
        user = user.scalar()
        if user:
            return UserDTO.from_orm(user)
        raise UserNotFoundError(id)

    async def update(self, user: UserDTO, dto: UpdateUserDTO) -> FullUserDTO:

        await self.session.execute(update(User).filter_by(email=user.email).values(**dto.dict()))
        await self.session.commit()

        user = await self.session.execute(select(User).filter_by(email=user.email))
        user = user.scalar()
    
        if user:
            return FullUserDTO.from_orm(user)
        raise UserNotFoundError(id)

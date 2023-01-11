from typing import List
from fastapi import Depends
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from internal.config.database import get_session
from internal.dto.user import CreateUserDTO, FullUserDTO, UpdateUserDTO, UserDTO

from internal.entity.user import User
from internal.exceptions.user import UserAlreadyExistsError, UserNotFoundError
from internal.util.hasher import Hasher


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

    async def create(self, dto: CreateUserDTO) -> UserDTO:
        user = User(**dto.dict())        

        user.password = Hasher.get_password_hash( user.password)

        try:
            self.session.add(user)
            await self.session.commit()

            return UserDTO.from_orm(user)

        except IntegrityError as exc:
            raise UserAlreadyExistsError(exc.params[0])

    async def update(self, id: str, dto: UpdateUserDTO) -> FullUserDTO:
        await self.session.execute(update(User).filter_by(id=id).values(**dto.dict()))
        await self.session.commit()

        user = await self.session.execute(select(User).filter_by(id=id))
        user = user.scalar()
    
        if user:
            return FullUserDTO.from_orm(user)
        raise UserNotFoundError(id)

from typing import List
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from internal.config.database import get_session
from internal.dto.user import CreateUserDTO, UserDTO

from internal.entity.user import User
from internal.exceptions.user import UserAlreadyExistsError, UserNotFoundError
from internal.util.uuid import is_valid_uuid

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

        try:
            self.session.add(user)
            await self.session.commit()

            return UserDTO.from_orm(user)

        except IntegrityError as exc:
            raise UserAlreadyExistsError(exc.params[0])

    async def update(self) -> UserDTO:
        return 
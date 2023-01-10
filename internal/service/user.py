from typing import List
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from internal.config.database import get_session
from internal.dto.user import CreateUserDTO, UserDTO

from internal.entity.user import User
from internal.exceptions.user import UserAlreadyExistsError

class UserService(object):
    def __init__(self, session: AsyncSession = Depends(get_session)) -> None:
        self.session = session

    async def get_all(self, limit: int = 10, offset: int = 0) -> List[UserDTO]:
        res = await self.session.execute(select(User).limit(limit).offset(offset))
        res = res.scalars().all()
        return res

    async def create(self, dto: CreateUserDTO) -> UserDTO:
        user = User(**dto.dict())
        print(user)

        try:
            self.session.add(user)
            self.session.commit()

            return UserDTO.from_orm(user)

        except IntegrityError as exc:
            print("#" * 30, exc.params[0])
            raise UserAlreadyExistsError(exc.params[0])
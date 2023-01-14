from fastapi import Depends

from typing import List

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from internal.config.database import get_session
from internal.entity.user import User
from internal.dto.user import UpdateUserDTO, UserDTO
from sqlalchemy.exc import IntegrityError

from internal.exceptions.user import UserAlreadyExistsError


class UserRepo(object):
    def __init__(
        self,
        session: AsyncSession = Depends(get_session), 
    ) -> None:
        self.sessin = session

    async def get_all(self, limit: int, offset: int) -> List[UserDTO]:
        res = await self.session.execute(select(User).limit(limit).offset(offset))
        return res.scalars().all()

    async def get_by_id(self, id: str) -> User:
        user = await self.session.execute(select(User).filter_by(id=id))
        return user.scalar()

    async def get_by_email(self, email: str) -> User:
        user = await self.session.execute(select(User).filter_by(email=email))
        return user.scalar()

    async def create(self, user: User) -> User:
        try:
            self.session.add(user)
            await self.session.commit()
        except IntegrityError as exc:
            raise UserAlreadyExistsError(exc.params[0])

        return user

    async def update(self, dto: UpdateUserDTO) -> User:
        user = await self.get_by_id(dto.id)

        if not user:
            return None

        await self.session.execute(update(User).filter_by(id=dto.id).values(**dto.dict()))
        await self.session.commit()

        user = await self.session.execute(select(User).filter_by(id=dto.id))
        return user.scalar()
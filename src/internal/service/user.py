from typing import List
from fastapi import Depends

from internal.config.redis import get_redis_session
from internal.config.database import get_repository
from internal.dto.user import UpdateUserDTO, UserDTO, UserAuthDTO
from internal.entity.user import User
from internal.exceptions.user import UserNotFoundError
from internal.repository.user import UserRepo
from internal.service.auth import get_current_user


class UserService(object):
    def __init__(
        self, 
        user_repo: UserRepo = Depends(get_repository(UserRepo)), 
        redis_session = Depends(get_redis_session),
        user: UserAuthDTO = Depends(get_current_user)
    ) -> None:
        self.repo = user_repo
        self.redis_session = redis_session
        self.user = user

    async def get_all(self, limit: int = 10, offset: int = 0) -> List[UserDTO]:
        return await self.repo.get_all(limit, offset)

    async def get(self) -> User:
        user = await self.repo.get_by_id(self.user.id)

        if user:
            return user
        raise UserNotFoundError(id)

    async def update(self, dto: UpdateUserDTO) -> User:
        user = await self.repo.update(dto)
    
        if user:
            return user
        raise UserNotFoundError(id)

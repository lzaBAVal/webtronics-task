from fastapi import Depends 

from internal.dto.post import PostDTO
from internal.entity.post import Post
from internal.config.database import get_session
from internal.exceptions.post import PostAlreadyExistsError

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError


class PostService(object):
    def __init__(self, session: AsyncSession = Depends(get_session)) -> None:
        self.session = session

    async def create(self, dto: PostDTO) -> PostDTO:
        post = Post(**dto.dict())

        try:
            self.session.add(post)
            await self.session.commit()

            return PostDTO.from_orm(post)

        except IntegrityError as exc:
            raise PostAlreadyExistsError(exc.params[0])

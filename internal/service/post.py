from typing import List
from uuid import UUID
from fastapi import Depends, Request
from sqlalchemy import select 

from internal.dto.post import PostDTO
from internal.dto.user import UserDTO
from internal.entity.post import Post
from internal.config.database import get_session
from internal.exceptions.post import PostAlreadyExistsError, PostNotFoundError
from internal.service.auth import get_current_user

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError


class PostService(object):
    def __init__(self, session: AsyncSession = Depends(get_session), user: UserDTO = Depends(get_current_user)) -> None:
        self.session = session
        self.user = user


    async def get_all(self) -> List[PostDTO]:
        posts = await self.session.execute(select(Post).filter_by(user_id=self.user.id))
        posts = posts.all()

        dtos = []
        for post in posts:
            dtos.append(PostDTO.from_orm(post[0]))

        return dtos


    async def create(self, dto: PostDTO) -> Post:
        post = Post(**dto.dict())
        post.user_id = self.user.id

        try:
            self.session.add(post)
            await self.session.commit()

            return post

        except IntegrityError as exc:
            raise PostAlreadyExistsError(exc.params[0])

    async def delete(self, uuid: str):
        post = await self.get_post(uuid)

        await self.session.delete(post)
        await self.session.commit()

    async def get_post(self, uuid: str) -> Post:
        post = await self.session.execute(select(Post).filter_by(user_id=self.user.id, id=uuid))
        post: Post = post.scalar()

        if not post:
            raise PostNotFoundError(uuid)
            
        return post
from typing import List
from uuid import UUID
from fastapi import Depends, Request
from sqlalchemy import select 

from internal.dto.post import PostDTO, CreatePostDTO
from internal.dto.user import UserDTO
from internal.entity.post import Post
from internal.config.database import get_session
from internal.exceptions.post import PostAlreadyExistsError, NoAccessManagePostError
from internal.repository.post import PostRepo
from internal.service.auth import get_current_user

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound


class PostService(object):
    def __init__(self, repo: PostRepo = Depends(), user: UserDTO = Depends(get_current_user)) -> None:
        self.repo = repo
        self.user = user


    async def get_all(self) -> List[PostDTO]:
        posts = await self.repo.get_by_user_id(self.user.id)

        dtos = []
        for post in posts:
            dtos.append(PostDTO.from_orm(post[0]))

        return dtos


    async def create(self, dto: CreatePostDTO) -> Post:
        try:
            return await self.repo.create(dto, self.user.id)
        except IntegrityError as exc:
            raise PostAlreadyExistsError(exc.params[0])

    async def delete(self, uuid: str):
        post = await self.repo.get_by_id(uuid)

        if post.user_id != self.user.id:
            raise NoAccessManagePostError(uuid)

        await self.repo.delete_by_id(uuid)


    async def get_post(self, uuid: str) -> Post:
        return await self.repo.get_by_id(uuid)
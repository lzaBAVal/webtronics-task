from fastapi import Depends

from typing import List

from sqlalchemy import delete, select, update

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import NoResultFound

from internal.config.database import get_session
from internal.dto.post import PostDTO, CreatePostDTO
from internal.entity.post import Post
from internal.exceptions.post import PostNotFoundError



class PostRepo(object):
    def __init__(
        self,
        session: AsyncSession = Depends(get_session), 
    ) -> None:
        self.sessin = session

    async def get_by_user_id(self, user_id: str) -> List[Post]:
        posts = await self.session.execute(select(Post).filter_by(user_id=user_id))
        return posts.all()

    async def create(self, dto: CreatePostDTO, user_id: str) -> Post:
        post = Post(**dto.dict())
        post.user_id = user_id

        self.session.add(post)
        await self.session.commit()

        return post
    
    async def get_by_id(self, id: str):
        post = await self.session.execute(select(Post).filter_by(id=id))
        post: Post = post.scalar()

        if not post:
            return PostNotFoundError

        return post

    async def delete_by_id(self, id: str):
        await self.session.execute(delete(Post).filter_by(id=id))
        await self.session.commit()
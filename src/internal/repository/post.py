from typing import List

from sqlalchemy import delete, select

from sqlalchemy.orm import Session

from internal.dto.post import CreatePostDTO
from internal.entity.post import Post
from internal.exceptions.post import PostNotFoundError
from internal.repository.base import BaseRepository



class PostRepo(BaseRepository):
    def __init__(self, session: Session) -> None:
        super().__init__(session)

    async def get_by_user_id(self, user_id: str) -> List[Post]:
        posts = await self.session.execute(select(Post).filter_by(user_id=user_id))
        return posts.all()

    async def create(self, dto: CreatePostDTO, user_id: str) -> Post:
        post = Post(**dto.dict())
        post.user_id = user_id

        self.session.add(post)
        await self.session.flush()

        return post
    
    async def get_by_id(self, id: str):
        post = await self.session.execute(select(Post).filter_by(id=id))
        post: Post = post.scalar()

        if not post:
            return PostNotFoundError

        return post

    async def delete_by_id(self, id: str):
        await self.session.execute(delete(Post).filter_by(id=id))
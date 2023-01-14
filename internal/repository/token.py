from fastapi import Depends

from typing import List

from sqlalchemy import delete, select, update

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import NoResultFound

from internal.config.database import get_session
from internal.dto.post import PostDTO, CreatePostDTO
from internal.entity.post import Post
from internal.entity.token import JWTToken



class TokenRepo(object):
    def __init__(
        self,
        session: AsyncSession = Depends(get_session), 
    ) -> None:
        self.sessin = session

    async def delete_by_user_id(self, user_id):
        await self.session.execute(delete(JWTToken).filter_by(user_id=user_id))
        await self.session.commit()

    async def add(self, token: JWTToken) -> JWTToken:
        self.session.add(token)
        await self.session.commit()

        return token
from asyncpg import Connection

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from internal.entity.token import JWTToken
from internal.repository.base import BaseRepository



class TokenRepo(BaseRepository):
    def __init__(self, session: Session) -> None:
        super().__init__(session)

    async def delete_by_user_id(self, user_id):
        await self.session.execute(delete(JWTToken).filter_by(user_id=user_id))

    async def add(self, token: JWTToken) -> JWTToken:
        self.session.add(token)

        return token

    async def get_by_token(self, token: str) -> JWTToken:
        token = await self.session.execute(select(JWTToken).filter_by(refresh_token=token))
        return token.scalar()
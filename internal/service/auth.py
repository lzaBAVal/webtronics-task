import time
import uuid

from datetime import timedelta, datetime
from aioredis import Redis

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from jose import JWTError, jwt
from pydantic import ValidationError

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from internal.config.redis import get_redis_session

from internal.dto.token import RefreshToken, Token, TokenPair
from internal.dto.user import CreateUserDTO, UserAuthDTO, UserDTO, UserPayloadDTO
from internal.entity.token import JWTToken
from internal.entity.user import User
from internal.exceptions.auth import NotValidRefreshTokenError, NotValidTokenError, RefreshTokenExpiredError
from internal.config.database import get_session
from internal.exceptions.user import UserAlreadyExistsError, UserNotFoundError, WrongUserPasswordError
from internal.config.config import config

from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/v1/auth/sign-in')


class AuthenticateService(object):
    def __init__(
        self, 
        session: AsyncSession = Depends(get_session), 
        redis_session: Redis = Depends(get_redis_session),
    ) -> None:
        self.session = session
        self.redis_session = redis_session

    @staticmethod
    def verify_password(plain: str, hashed: str):
        return pwd_context.verify(plain, hashed)

    @staticmethod
    def get_password_hash(plain):
        return pwd_context.hash(plain)       
    
    @staticmethod
    def decode_token(token: str) -> UserPayloadDTO:
        try:
            payload = jwt.decode(
                token,
                config.jwt.secret,
                algorithms=config.jwt.algorithm,
            )
        except JWTError:
            raise NotValidTokenError

        user_data = payload.get('user')

        try:
            user = UserDTO.parse_obj(user_data)
        except ValidationError:
            raise NotValidTokenError

        return UserPayloadDTO(
            iat=payload.get('iat'),
            exp=payload.get('exp'),
            sub=payload.get('sub'),
            user=user
        )

        

    async def create_access_token(self, user: User) -> Token:
        user_data = UserDTO.from_orm(user)
        now = datetime.utcnow()

        payload = {
            'iat': now,
            'exp': now + timedelta(seconds=config.jwt.expires_sec),
            'sub': str(user.id),
            'user': user_data.dict(),
        }

        token = jwt.encode(
            payload,
            config.jwt.secret,
            algorithm=config.jwt.algorithm,
        )

        return Token(access_token=token)

    async def verify_token(self, token: str) -> UserDTO:
        payload: UserPayloadDTO = self.decode_token(token)

        if await self.check_token_blacklist(payload, token):
            raise NotValidTokenError

        return payload.user

    async def check_token_blacklist(self, dto: UserPayloadDTO, token: str):
        blacklist_token = await self.redis_session.get(str(dto.user.email))
        return blacklist_token == token

    async def delete_refresh_token(self, user_id: str) -> None:
        await self.session.execute(delete(JWTToken).filter_by(user_id=user_id))
        await self.session.commit()
    
    async def create_refresh_token(self, user: User) -> RefreshToken:
        token_hex = uuid.uuid4().hex

        token = JWTToken()
        token.user_id = user.id
        token.refresh_token=token_hex

        await self.delete_refresh_token(user.id)

        self.session.add(token)
        await self.session.commit()

        return RefreshToken(token=token.refresh_token)

    async def register_user(self, dto: CreateUserDTO) -> Token:
        user = User(**dto.dict())

        user.password = self.get_password_hash( user.password)

        try:
            self.session.add(user)
            await self.session.commit()
        except IntegrityError as exc:
            raise UserAlreadyExistsError(exc.params[0])

        return await self.create_tokens(user)

    async def authenticate_user(self, dto: UserAuthDTO) -> TokenPair:
        user = await self.session.execute(select(User).filter_by(email=dto.username))
        user: User = user.scalar()

        if not user:
            raise UserNotFoundError
        
        if not self.verify_password(dto.password, user.password):
            raise WrongUserPasswordError

        return await self.create_tokens(user) 

    async def refresh_tokens(self, refresh_token: RefreshToken) -> TokenPair:
        token = await self.session.execute(select(JWTToken).filter_by(refresh_token=refresh_token.token))
        token: JWTToken = token.scalar()

        if not token:
            raise NotValidRefreshTokenError

        print("token.ttl:", token.ttl)

        if datetime.now() > token.ttl:
            raise RefreshTokenExpiredError

        user = await self.session.execute(select(User).filter_by(id=token.user_id))

        return await self.create_tokens(user.scalar())

    async def create_tokens(self, user: User) -> TokenPair:
        refresh_token = await self.create_refresh_token(user)
        access_token = await self.create_access_token(user)

        return TokenPair(
            access_token=access_token, 
            refresh_token=refresh_token
        )   

    async def delete_tokens(self, token: str):
        payload = self.decode_token(token)

        await self.delete_refresh_token(payload.sub)
        await self.add_token_blacklist(token)
        
    async def add_token_blacklist(self, token: str):
        payload = self.decode_token(token)

        print(payload.exp, time.time())
        await self.redis_session.setex(payload.user.email, int(payload.exp - time.time()), token)


async def get_current_user(token: str = Depends(oauth2_scheme), auth_service: AuthenticateService = Depends()) -> UserDTO:
    return await auth_service.verify_token(token)


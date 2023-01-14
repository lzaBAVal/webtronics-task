import time
import uuid

from datetime import timedelta, datetime
from aioredis import Redis

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from jose import JWTError, jwt
from pydantic import ValidationError

from internal.config.redis import get_redis_session

from internal.dto.token import RefreshToken, Token, TokenPair
from internal.dto.user import CreateUserDTO, UserAuthDTO, UserDTO, UserPayloadDTO
from internal.entity.token import JWTToken
from internal.entity.user import User
from internal.exceptions.auth import NotValidRefreshTokenError, NotValidTokenError, RefreshTokenExpiredError
from internal.config.database import get_session
from internal.exceptions.user import UserNotFoundError, WrongUserPasswordError
from internal.config.config import config

from passlib.context import CryptContext

from internal.repository.token import TokenRepo
from internal.repository.user import UserRepo


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/v1/auth/sign-in')

BIGINT = 2 ** 32-1

class AuthenticateService(object):
    def __init__(
        self, 
        token_repo: TokenRepo = Depends(), 
        user_repo: UserRepo = Depends(),
        redis_session: Redis = Depends(get_redis_session),
    ) -> None:
        self.token_repo = token_repo
        self.user_repo = user_repo
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

    @staticmethod
    def encode_token(dto: UserDTO) -> str:
        now = datetime.utcnow()

        dto.id = str(dto.id)

        payload = {
            'iat': now,
            'exp': now + timedelta(seconds=config.jwt.expires_sec),
            'sub': 'auth',
            'user': dto.dict(),
        }

        token = jwt.encode(
            payload,
            config.jwt.secret,
            algorithm=config.jwt.algorithm,
        )

        return token

    async def create_access_token(self, user: User) -> Token:
        user_data = UserDTO.from_orm(user)
        token = self.encode_token(user_data)

        return Token(access_token=token)


    async def verify_token(self, token: str) -> UserDTO:
        payload: UserPayloadDTO = self.decode_token(token)

        if await self.check_token_blacklist(payload, token):
            raise NotValidTokenError

        return payload.user


    async def check_token_blacklist(self, dto: UserPayloadDTO, token: str):
        blacklist_token = await self.redis_session.zrangebyscore(dto.user.email, int(time.time()), BIGINT)
        return token in blacklist_token


    async def delete_refresh_token(self, user_id: str) -> None:
        await self.repo.delete_by_user_id(user_id)


    async def create_refresh_token(self, user: User) -> RefreshToken:
        token = JWTToken()
        token.user_id = user.id
        token.refresh_token=uuid.uuid4().hex

        await self.token_repo.delete_by_user_id(user.id)
        token = await self.token_repo.add(token)

        return RefreshToken(token=token.refresh_token)


    async def register_user(self, dto: CreateUserDTO) -> Token:
        user = User(**dto.dict())
        user.password = self.get_password_hash( user.password)
        user = await self.user_repo.create(user)

        return await self.create_tokens(user)


    async def authenticate_user(self, dto: UserAuthDTO) -> TokenPair:
        user = await self.user_repo.get_by_email(str(dto.email))

        if not user:
            raise UserNotFoundError
        
        if not self.verify_password(dto.password, user.password):
            raise WrongUserPasswordError

        return await self.create_tokens(user) 


    async def refresh_tokens(self, refresh_token: RefreshToken) -> TokenPair:
        token = await self.token_repo.get_by_token(refresh_token.token)

        if not token:
            raise NotValidRefreshTokenError

        if datetime.now() > token.ttl:
            raise RefreshTokenExpiredError

        user = await self.user_repo.get_by_id(token.user_id)

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
        await self.add_access_token_blacklist(token)
        

    async def add_access_token_blacklist(self, token: str):
        payload = self.decode_token(token)
        await self.redis_session.zadd(payload.user.email, {token: payload.exp})


async def get_current_user(token: str = Depends(oauth2_scheme), auth_service: AuthenticateService = Depends()) -> UserDTO:
    return await auth_service.verify_token(token)

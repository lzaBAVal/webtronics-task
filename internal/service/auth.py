import uuid

from datetime import timedelta, datetime

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from jose import JWTError, jwt
from pydantic import ValidationError

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from internal.dto.token import RefreshToken, Token, TokenPair
from internal.dto.user import CreateUserDTO, UserAuthDTO, UserDTO
from internal.entity.token import JWTToken
from internal.entity.user import User
from internal.exceptions.auth import NotValidRefreshTokenError, NotValidTokenError, RefreshTokenExpiredError
from internal.config.database import get_session
from internal.exceptions.user import UserAlreadyExistsError, UserNotFoundError, WrongUserPasswordError
from internal.config.config import config

from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/v1/auth/sign-in')


def get_current_user(token: str = Depends(oauth2_scheme)) -> UserDTO:
    print("token:", token)
    return AuthenticateService.verify_token(token)


class AuthenticateService(object):
    def __init__(self, session: AsyncSession = Depends(get_session)) -> None:
        self.session = session

    @staticmethod
    def verify_password(plain: str, hashed: str):
        return pwd_context.verify(plain, hashed)

    @staticmethod
    def get_password_hash(plain):
        return pwd_context.hash(plain)       
    
    async def create_access_token(self, user: User) -> Token:
        user_data = UserDTO.from_orm(user)
        now = datetime.utcnow()
        payload = {
            'iat': now,
            'nbf': now,
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

    @classmethod
    def verify_token(cls, token: str) -> UserDTO:
        print("#"*30, token)
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

        return user

    async def delete_refresh_token(self, user: User) -> None:
        await self.session.execute(delete(JWTToken).filter_by(user_id=user.id))
        await self.session.commit()
    
    async def create_refresh_token(self, user: User) -> RefreshToken:
        token_hex = uuid.uuid4().hex

        token = JWTToken()
        token.user_id = user.id
        token.refresh_token=token_hex

        await self.delete_refresh_token(user)

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
        
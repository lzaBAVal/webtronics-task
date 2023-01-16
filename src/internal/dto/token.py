from pydantic import BaseModel


class AccessToken(BaseModel):
    token: str
    token_type: str = 'bearer'


class RefreshToken(BaseModel):
    token: str


class TokenPair(BaseModel):
    access_token: AccessToken
    refresh_token: RefreshToken
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class RefreshToken(BaseModel):
    refresh_token: str


class TokenPair(Token):
    access_token: Token
    refresh_token: RefreshToken
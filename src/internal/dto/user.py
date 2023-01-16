from dataclasses import dataclass

from fastapi import Form, Path

from pydantic import BaseModel, EmailStr
from uuid import UUID

class UserDTO(BaseModel):
    id: UUID
    email: EmailStr

    class Config:
        allow_mutations = False
        orm_mode = True


class UserAuthDTO(BaseModel):
    username: EmailStr
    password: str


class CreateUserForm:
    def __init__(
        self,
        email: EmailStr = Form(),
        password: str   = Form()
    ) -> None:
        self.email = email
        self.password = password
        
    


class UpdateUserDTO(BaseModel):
    email: EmailStr
    password: str


class UserPayloadDTO(BaseModel):
    iat: int
    exp: int
    sub: str
    user: UserDTO


@dataclass
class UserFilter(object):
    username: str = Path(title="The name of user to get")
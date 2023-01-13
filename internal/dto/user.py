from dataclasses import dataclass

from fastapi import Path

from pydantic import BaseModel, EmailStr
from uuid import UUID

class UserDTO(BaseModel):
    id: UUID
    email: EmailStr

    class Config:
        allow_mutations = False
        orm_mode = True


class UserAuthDTO(UserDTO):
    password: str


class CreateUserDTO(UserDTO):
    password: str


class UpdateUserDTO(CreateUserDTO):
    pass


class UserPayloadDTO(BaseModel):
    iat: int
    exp: int
    sub: str
    user: UserDTO


@dataclass
class UserFilter(object):
    username: str = Path(title="The name of user to get")
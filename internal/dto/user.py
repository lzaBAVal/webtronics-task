from dataclasses import dataclass

from fastapi import Path

from pydantic import BaseModel, EmailStr


class UserDTO(BaseModel):
    username: str
    email: EmailStr

    class Config:
        allow_mutations = False
        orm_mode = True


class CreateUserDTO(UserDTO):
    password: str


@dataclass
class UserFilter(object):
    username: str = Path(title="The name of user to get")
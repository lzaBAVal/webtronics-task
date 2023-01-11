from dataclasses import dataclass

from fastapi import Path

from pydantic import BaseModel, EmailStr
from uuid import UUID

class UserDTO(BaseModel):
    username: str

    class Config:
        allow_mutations = False
        orm_mode = True


class CreateUserDTO(UserDTO):
    password: str


class UpdateUserDTO(CreateUserDTO):
    email: EmailStr


class FullUserDTO(UpdateUserDTO):
    id: UUID


@dataclass
class UserFilter(object):
    username: str = Path(title="The name of user to get")
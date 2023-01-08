from dataclasses import dataclass
from datetime import date

from fastapi import Path

from pydantic import BaseModel


class UserDTO(BaseModel):
    username: str
    email: str

    class Config:
        allow_mutations = False


@dataclass
class UserFilter(object):
    username: str = Path(title="The name of user to get")
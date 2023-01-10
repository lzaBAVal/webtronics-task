from typing import Any
from fastapi import APIRouter, Depends
from internal.dto.user import CreateUserDTO, UserDTO

from internal.service.user import UserService

router = APIRouter()

@router.get('/', response_model=list[UserDTO])
async def get_all_uesrs(user_service: UserService = Depends()) -> Any:
    users = await user_service.get_all()
    return users


@router.post('/', response_model=UserDTO)
async def create_new_user(new_user: CreateUserDTO, user_service: UserService = Depends()) -> Any:
    user = await user_service.create(new_user)
    return user
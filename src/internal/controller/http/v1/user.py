from typing import Any
from fastapi import APIRouter, Depends
from internal.dto.user import UpdateUserDTO, UserDTO

from internal.service.user import UserService


router = APIRouter()


@router.get('/all', response_model=list[UserDTO])
async def get_all_uesrs(user_service: UserService = Depends()) -> Any:
    return await user_service.get_all()


@router.get('/me', response_model=UserDTO)
async def get_me(user_service: UserService = Depends()) -> Any:
    return await user_service.get()   


@router.patch('/{id}', response_model=UserDTO)
async def update_user(dto: UpdateUserDTO, user_service: UserService = Depends()) -> Any:
    return await user_service.update(dto)
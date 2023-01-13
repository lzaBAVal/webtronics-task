from typing import Any
from fastapi import APIRouter, Depends
from internal.dto.user import UpdateUserDTO, UserDTO

from internal.service.user import UserService
from internal.service.auth import get_current_user


router = APIRouter()


@router.get('/all', response_model=list[UserDTO])
async def get_all_uesrs(user_service: UserService = Depends()) -> Any:
    return await user_service.get_all()


@router.get('/me', response_model=UserDTO)
async def get_me(user: UserDTO = Depends(get_current_user)) -> Any:
    return user


@router.patch('/{id}', response_model=UserDTO)
async def update_user(dto: UpdateUserDTO, user_service: UserService = Depends(), user: UserDTO = Depends(get_current_user)) -> Any:
    return await user_service.update(user, dto)
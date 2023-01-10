from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from internal.dto.user import CreateUserDTO, UserDTO
from internal.exceptions.user import UserAlreadyExistsError

from internal.service.user import UserService

router = APIRouter()

@router.get('/', response_model=list[UserDTO])
async def get_all_uesrs(user_service: UserService = Depends()) -> Any:
    return await user_service.get_all()


@router.post('/', response_model=UserDTO)
async def create_new_user(dto: CreateUserDTO, user_service: UserService = Depends()) -> Any:
    try:
        return await user_service.create(dto)
    except UserAlreadyExistsError as exc:
        raise HTTPException(409, str(exc))
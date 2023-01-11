from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from internal.dto.user import CreateUserDTO, FullUserDTO, UpdateUserDTO, UserDTO
from internal.exceptions.type import UUIDWrongTypeError
from internal.exceptions.user import UserAlreadyExistsError, UserNotFoundError

from internal.service.user import UserService
from internal.service.auth import AuthenticateService
from internal.util.uuid import is_valid_uuid
from internal.service.auth import get_current_user

router = APIRouter()

@router.get('/all', response_model=list[UserDTO])
async def get_all_uesrs(user_service: UserService = Depends()) -> Any:
    return await user_service.get_all()


@router.post('/', response_model=UserDTO)
async def create_new_user(dto: CreateUserDTO, user_service: UserService = Depends()) -> Any:
    try:
        return await user_service.create(dto)
    except UserAlreadyExistsError as exc:
        raise HTTPException(409, str(exc))


@router.get('/me', response_model=UserDTO)
async def get_me(user: UserDTO = Depends(get_current_user)) -> Any:
    return user


@router.patch('/{id}', response_model=FullUserDTO)
async def update_user(id: str, dto: UpdateUserDTO, user_service: UserService = Depends()) -> Any:
    if not is_valid_uuid(id):
        raise HTTPException(422, str(UUIDWrongTypeError(id)))

    try:
        return await user_service.update(id, dto)
    except UserNotFoundError as exc:
        raise HTTPException(404, str(exc))
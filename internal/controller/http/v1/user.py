from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from internal.dto.user import CreateUserDTO, UserDTO
from internal.exceptions.type import UUIDWrongTypeError
from internal.exceptions.user import UserAlreadyExistsError, UserNotFoundError

from internal.service.user import UserService
from internal.util.uuid import is_valid_uuid

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


@router.get('/{id}', response_model=UserDTO)
async def get_by_id(id: str, user_service: UserService = Depends()) -> Any:
    if not is_valid_uuid(id):
        raise HTTPException(422, str(UUIDWrongTypeError(id)))

    try:
        return await user_service.get(id)
    except UserNotFoundError as exc:
        raise HTTPException(404, str(exc))
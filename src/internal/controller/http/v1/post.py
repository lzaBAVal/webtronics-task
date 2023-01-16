from typing import Any, List
from uuid import UUID
from fastapi import APIRouter, Depends

from internal.dto.post import CreatePostDTO, PostDTO
from internal.exceptions.type import UUIDWrongTypeError
from internal.service.post import PostService
from internal.util.uuid import is_valid_uuid


router = APIRouter()


@router.get('/all', response_model=List[PostDTO])
async def get_all(post_service: PostService = Depends()) -> Any:
    return await post_service.get_all()


@router.post('/', response_model=PostDTO)
async def create(dto: CreatePostDTO, post_service: PostService = Depends()) -> Any:
    return await post_service.create(dto)


@router.delete('/{uuid}')
async def delete(uuid: str, post_service: PostService = Depends()) -> Any:
    if not is_valid_uuid(uuid):
        raise UUIDWrongTypeError(uuid)

    await post_service.delete(uuid)


@router.get('/{uuid}', response_model=PostDTO)
async def delete(uuid: str, post_service: PostService = Depends()) -> Any:
    if not is_valid_uuid(uuid):
        raise UUIDWrongTypeError(uuid)

    await post_service.get_post(uuid)

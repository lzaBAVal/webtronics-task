from typing import Any
from fastapi import APIRouter, Depends
from internal.dto.user import UserDTO

from internal.service.user import UserService

router = APIRouter()

@router.get('/', response_model=list[UserDTO])
async def get_all_uesrs(user_service: UserService = Depends()) -> Any:
    users = await user_service.get_all()
    print(users)
    return users
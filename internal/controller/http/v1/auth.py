from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from internal.dto.token import Token
from internal.dto.user import CreateUserDTO, UserAuthDTO
from internal.service.auth import AuthenticateService


router = APIRouter()

@router.post('/sign-up', response_model=Token, status_code=status.HTTP_201_CREATED)
async def sign_up(form_data: CreateUserDTO = Depends(), auth_service: AuthenticateService = Depends()):
    return await auth_service.register_user(form_data)

@router.post('/sign-in', response_model=Token)
async def sign_in(form_data: OAuth2PasswordRequestForm = Depends(), auth_service: AuthenticateService = Depends()):
    return await auth_service.authenticate_user(form_data)


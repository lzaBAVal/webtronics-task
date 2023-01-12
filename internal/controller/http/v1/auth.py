from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from internal.dto.token import RefreshToken, TokenPair
from internal.dto.user import CreateUserDTO
from internal.service.auth import AuthenticateService


router = APIRouter()

@router.post('/sign-up', response_model=TokenPair, status_code=status.HTTP_201_CREATED)
async def sign_up(form_data: CreateUserDTO = Depends(), auth_service: AuthenticateService = Depends()):
    return await auth_service.register_user(form_data)

@router.post('/sign-in', response_model=TokenPair)
async def sign_in(form_data: OAuth2PasswordRequestForm = Depends(), auth_service: AuthenticateService = Depends()):
    pair = await auth_service.authenticate_user(form_data)
    return pair

@router.post('/refresh-token', response_model=TokenPair)
async def refresh_token(refresh_token: RefreshToken, auth_service: AuthenticateService = Depends()):
    return await auth_service.refresh_tokens(refresh_token)
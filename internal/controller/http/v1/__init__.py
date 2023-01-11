from fastapi import APIRouter

from . import user, auth

router = APIRouter()
router.include_router(
    user.router,
    prefix='/user',
    tags=['users'],
)

router.include_router(
    auth.router,
    prefix='/auth',
    tags=['auth'],
)
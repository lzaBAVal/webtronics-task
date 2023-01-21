from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from internal.controller.http import v1
from internal.repository.user import UserRepo
from internal.config.database import get_repository


api_router = APIRouter()
api_router.include_router(v1.router, prefix="/v1")


@api_router.get('/ping', response_class=JSONResponse)
async def ping(user_repo: UserRepo = Depends(get_repository(UserRepo))):
    print(await user_repo.get_all())
    return JSONResponse({"answer": "pong"}, 200)
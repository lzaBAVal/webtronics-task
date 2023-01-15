from fastapi import APIRouter
from fastapi.responses import JSONResponse

from internal.controller.http import v1

api_router = APIRouter()
api_router.include_router(v1.router, prefix="/v1")


@api_router.get('/ping', response_class=JSONResponse)
async def ping():
    return JSONResponse({"answer": "pong"}, 200)
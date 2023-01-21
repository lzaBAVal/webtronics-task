from typing import Callable
from fastapi import FastAPI

from internal.config.config import Config
from internal.config.database import connect_to_db, close_db_connection

def start_app_handler(app: FastAPI, config: Config) -> Callable:
    async def start_app():
        pass
    return start_app


def stop_app_handler(app: FastAPI) -> Callable:
    async def stop_app():
        pass

    return stop_app
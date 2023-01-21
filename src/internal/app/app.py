from fastapi import FastAPI

from internal.config.app_handlers import start_app_handler, stop_app_handler
from internal.controller.http.router import api_router
from internal.config.config import get_config


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(api_router)

    config = get_config()
    app.state.config = config

    # app.add_event_handler("startup", start_app_handler(app, config))
    # app.add_event_handler("shutdown", stop_app_handler(app))

    return app

from fastapi import HTTPException, status


class PostAlreadyExistsError(HTTPException):
    def __init__(self, msg: str) -> None:
        self.status_code = status.HTTP_409_CONFLICT
        self.detail = f"Post already exists: {msg}"
        
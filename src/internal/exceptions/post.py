
from fastapi import HTTPException, status


class PostAlreadyExistsError(HTTPException):
    def __init__(self, msg: str) -> None:
        self.status_code = status.HTTP_409_CONFLICT
        self.detail = f"Post already exists: {msg}"
        

class PostNotFoundError(HTTPException):
    def __init__(self, msg: str) -> None:
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = f"Post with UUID '{msg}' not found"
        

class NoAccessManagePostError(HTTPException):
    def __init__(self, msg: str) -> None:
        self.status_code = status.HTTP_403_FORBIDDEN
        self.detail = f"You haven't access to manage this post '{msg}'"
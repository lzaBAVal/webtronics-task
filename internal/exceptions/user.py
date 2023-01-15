from fastapi import HTTPException, status


class UserAlreadyExistsError(Exception):
    def __init__(self, email: str) -> None:
        self.status_code = status.HTTP_409_CONFLICT
        self.detail = f"User with this email '{email}' already exists."

class UserNotFoundError(HTTPException):
    def __init__(self) -> None:
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = f"User not found with id"


class WrongUserPasswordError(Exception):
    def __init__(self) -> None:
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = f"Wrong email or password"
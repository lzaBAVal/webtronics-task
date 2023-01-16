from fastapi import HTTPException, status


class NotValidTokenError(HTTPException):
    def __init__(self) -> None:
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail ='Could not validate credentials'
        self.headers = {'WWW-Authenticate': 'Bearer'}


class NotValidRefreshTokenError(HTTPException):
    def __init__(self) -> None:
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = 'Not valid refresh token'
        self.headers = {'WWW-Authenticate': 'Bearer'}


class RefreshTokenExpiredError(HTTPException):
    def __init__(self) -> None:
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = 'Refresh token expired'
        self.headers = {'WWW-Authenticate': 'Bearer'}

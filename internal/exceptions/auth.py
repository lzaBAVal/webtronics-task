from fastapi import HTTPException, status


class NotValidTokenError(HTTPException):
    def __init__(self) -> None:
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail ='Could not validate credentials'
        self.headers = {'WWW-Authenticate': 'Bearer'}

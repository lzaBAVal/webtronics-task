from fastapi import HTTPException, status


class UUIDWrongTypeError(HTTPException):
    def __init__(self, id: str) -> None:
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = f"Id '{id}' is not UUID"

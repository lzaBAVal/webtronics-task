class UserAlreadyExistsError(Exception):
    def __init__(self, email: str) -> None:
        super().__init__(f"User with this email '{email}' already exists.")


class UserNotFoundError(Exception):
    def __init__(self, id: str) -> None:
        super().__init__(f"User not found with id '{id}'")


class WrongUserPasswordError(Exception):
    def __init__(self) -> None:
        super().__init__(f"Wrong password")
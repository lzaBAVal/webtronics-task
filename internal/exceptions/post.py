
class PostAlreadyExistsError(Exception):
    def __init__(self, msg: str) -> None:
        super().__init__(f"Post already exists: {msg}")
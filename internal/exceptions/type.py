class UUIDWrongTypeError(Exception):
    def __init__(self, id: str) -> None:
        super().__init__(f"Id '{id}' is not UUID")
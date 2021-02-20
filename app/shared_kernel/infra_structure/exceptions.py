class ResourceNotFoundError(Exception):
    def __init__(self, msg: str = "") -> None:
        super().__init__(msg)


class ResourceAlreadyExistError(Exception):
    def __init__(self, msg: str = "") -> None:
        super().__init__(msg)

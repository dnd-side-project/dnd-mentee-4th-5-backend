class UserAlreadyExistError(Exception):
    def __init__(self, msg: str) -> None:
        self.msg = msg


class UserNotExistError(Exception):
    def __init__(self, msg: str) -> None:
        self.msg = msg

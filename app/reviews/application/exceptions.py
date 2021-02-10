class ReviewNotExistError(Exception):
    def __init__(self, msg: str) -> None:
        self.msg = msg


class ReviewAlreadyExistError(Exception):
    def __init__(self, msg: str) -> None:
        self.msg = msg

from fastapi import HTTPException

from config import MAX_AVATAR_SIZE


class AlreadyRegisteredException(HTTPException):
    def __init__(self) -> None:
        super().__init__(403, "Already registered")

class FileSizeException(HTTPException):
    def __init__(self) -> None:
        super().__init__(400, "Exceeded max file size (limit %s KB)" % (MAX_AVATAR_SIZE / 1024))

class InvalidImageException(HTTPException):
    def __init__(self) -> None:
        super().__init__(400, "Invalid image file")

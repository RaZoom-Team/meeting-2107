from config import MAX_AVATAR_SIZE
from infrastructure.exc.basic import ErrorCode, HTTPError


class AlreadyRegisteredException(HTTPError):
    def __init__(self) -> None:
        super().__init__(403, ErrorCode.E3001_ALREADY_REG, "Already registered")

class FileSizeException(HTTPError):
    def __init__(self) -> None:
        super().__init__(400, ErrorCode.E2002_FILESIZE, "Exceeded max file size (limit %s KB)" % (MAX_AVATAR_SIZE / 1024))

class InvalidImageException(HTTPError):
    def __init__(self) -> None:
        super().__init__(400, ErrorCode.E2003_BADIMG, "Invalid image file")

class VerifyRestrictionsException(HTTPError):
    def __init__(self) -> None:
        super().__init__(403, ErrorCode.E3002_VERIFY_RESTRICTION, "Verify can not change name, surname, literal and male")
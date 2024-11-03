from urllib.parse import quote

from config import MAX_AVATAR_SIZE, TG_CHANNEL_LINK
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

class SubscriptionRequiredException(HTTPError):
    def __init__(self) -> None:
        super().__init__(403, ErrorCode.E3004_SUBSCRIPTION_REQ, "Subscription to channel required", headers={"X-Channel": TG_CHANNEL_LINK})

class BannedException(HTTPError):
    def __init__(self, reason: str) -> None:
        super().__init__(403, ErrorCode.E3005_BANNED, "Your account has been banned", headers={"X-Reason": quote(reason)})

class AlreadyVerifiedException(HTTPError):
    def __init__(self) -> None:
        super().__init__(403, ErrorCode.E3006_ALREADY_VERIFY, "You already verified")

from .basic import ErrorCode, HTTPError


class AuthDataException(HTTPError):
    def __init__(self) -> None:
        super().__init__(400, ErrorCode.E2000_INVALID_TDATA, "Invalid Telegram Data")

class UnregisteredException(HTTPError):
    def __init__(self) -> None:
        super().__init__(401, ErrorCode.E3000_UNREGISTERED, "This account is not registered")

class UsernameRequired(HTTPError):
    def __init__(self) -> None:
        super().__init__(400, ErrorCode.E2001_USERNAME_REQ, "Username required")
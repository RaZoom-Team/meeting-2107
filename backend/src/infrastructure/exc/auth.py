from typing import Any, Dict
from typing_extensions import Annotated, Doc
from fastapi import HTTPException


class AuthDataException(HTTPException):
    def __init__(self) -> None:
        super().__init__(401, "Invalid Telegram Data")

class UnregisteredException(HTTPException):
    def __init__(self) -> None:
        super().__init__(401, "This account is not registered")
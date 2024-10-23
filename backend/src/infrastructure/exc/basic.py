from typing import Any, Dict
from typing_extensions import Annotated, Doc
from fastapi import HTTPException


class NotFound(HTTPException):
    def __init__(self) -> None:
        super().__init__(404, "Not found")
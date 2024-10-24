from typing import Any, Dict
from typing_extensions import Annotated, Doc
from fastapi import HTTPException


class FocusNotSelected(HTTPException):
    def __init__(self) -> None:
        super().__init__(403, "Focus user not selected")
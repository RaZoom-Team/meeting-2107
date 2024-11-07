from typing import Literal
from pydantic import BaseModel, Field


class GetUsersArgs(BaseModel):
    filter: Literal["all", "banned", "verify"] = "all"

class GetUsers(GetUsersArgs):
    offset: int = 0
    limit: int = Field(gt = 1, le=50)

class UserRequest(BaseModel):
    user_id: int

class ReasonRequest(UserRequest):
    reason: str

class VerifyUser(UserRequest):
    value: bool

class GetUserResponse(BaseModel):
    text: str
    attachments: list[str]

class GetUsersResponse(BaseModel):
    text: str
    count: int

class RequestResponse[T: BaseModel](BaseModel):
    success: bool
    error: str | None
    response: T | None
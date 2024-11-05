from pydantic import BaseModel


class UserRequest(BaseModel):
    user_id: int

class ReasonRequest(UserRequest):
    reason: str

class VerifyUser(UserRequest):
    value: bool

class GetUserResponse(BaseModel):
    text: str
    attachments: list[str]

class RequestResponse[T: BaseModel](BaseModel):
    success: bool
    error: str | None
    response: T | None
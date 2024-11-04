from pydantic import BaseModel


class TelegramRequest(BaseModel):
    msg_id: int

class UnbanUser(TelegramRequest):
    user_id: int

class BanUser(UnbanUser):
    reason: str

class VerifyUser(TelegramRequest):
    user_id: int
    value: bool

class GetUser(TelegramRequest):
    user_id: int

class TelegramRequestResponse(TelegramRequest):
    success: bool

class GetUserResponse(TelegramRequestResponse):
    text: str
    attachments: list[str]
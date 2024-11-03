from pydantic import BaseModel


class BanUser(BaseModel):
    msg_id: int
    user_id: int
    reason: str

class BannedUser(BaseModel):
    msg_id: int
    success: bool

class VerifyUser(BaseModel):
    msg_id: int
    user_id: int
    value: bool

class VerifiedUser(BaseModel):
    msg_id: int
    sucess: bool
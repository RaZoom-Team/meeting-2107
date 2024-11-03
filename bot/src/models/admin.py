from pydantic import BaseModel


class BanUser(BaseModel):
    msg_id: int
    user_id: int
    reason: str

class BannedUser(BaseModel):
    msg_id: int
    success: bool
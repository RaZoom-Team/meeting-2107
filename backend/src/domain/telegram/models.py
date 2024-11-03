from pydantic import BaseModel


class SendTelegramMessage(BaseModel):
    chat_id: int
    text: str
    parse_mode: str = "html"

class SendMediaTelegramMessage(SendTelegramMessage):
    files: list[str]
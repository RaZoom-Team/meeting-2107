from typing import Literal
from pydantic import BaseModel


class SendMessage(BaseModel):
    chat_id: int
    text: str
    parse_mode: str = "html"

class SendAdminMessage(SendMessage):
    chat_id: Literal[-1]

class SendMediaMessage(SendMessage):
    files: list[str]

class SendAdminMediaMessage(SendAdminMessage, SendMediaMessage):
    pass
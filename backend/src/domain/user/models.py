from pydantic import BaseModel, Field, field_validator

from config import API_URL, CLASS_LITERAL
from infrastructure.db import Attachment


class BaseUser(BaseModel):
    name: str = Field(max_length=64, examples=["Иван"])
    surname: str = Field(max_length=64, examples=["Иванов"])
    desc: str = Field(max_length=128, examples=["Главный айтишник класса"])
    literal: CLASS_LITERAL
    male: bool

class UserDTO(BaseUser):
    is_active: bool
    attachments: list[str] = Field(examples=[[f"{API_URL}/attachments/abcde1234567890"]])

    @field_validator("attachments", mode="before")
    @classmethod
    def test_validator(cls, attachments: list[str] | list[Attachment]):
        if attachments and isinstance(attachments[0], Attachment):
            return [atch.url for atch in attachments]
        return attachments
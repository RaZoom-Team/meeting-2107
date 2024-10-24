from pydantic import BaseModel, Field, field_validator

from config import API_URL, CLASS_LITERAL
from infrastructure.db import Attachment


class BaseUser(BaseModel):
    name: str = Field(max_length=64, examples=["Иван"], description="Имя")
    surname: str = Field(max_length=64, examples=["Иванов"], description="Фамилия")
    desc: str = Field(max_length=128, examples=["Главный айтишник класса"], description="Описание")
    literal: CLASS_LITERAL = Field(description="Класс")
    male: bool = Field(description="Пол (мужчина или нет)")

class UserDTO(BaseUser):
    attachments: list[str] = Field(examples=[[f"{API_URL}/attachments/abcde1234567890"]], description="Вложения пользователя")

    @field_validator("attachments", mode="before")
    @classmethod
    def test_validator(cls, attachments: list[str] | list[Attachment]):
        if attachments and isinstance(attachments[0], Attachment):
            return [atch.url for atch in attachments]
        return attachments

class FullUserDTO(UserDTO):
    is_active: bool = Field(description="Активна-ли анкета")
    focus_user: UserDTO | None = Field(description="Текущая просматриваемая анкета")
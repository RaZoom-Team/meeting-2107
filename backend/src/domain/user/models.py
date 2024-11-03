from fastapi import HTTPException
from pydantic import BaseModel, Field, field_validator

from config import API_URL, CLASS_LITERAL
from infrastructure.db import Attachment
from infrastructure.utils import partial_model


class BaseUser(BaseModel):
    name: str = Field(min_length=3, max_length=21, examples=["Иван"], description="Имя")
    surname: str = Field(min_length=3, max_length=21, examples=["Иванов"], description="Фамилия")
    desc: str = Field(max_length=300, examples=["Главный айтишник класса"], description="Описание")
    literal: CLASS_LITERAL = Field(description="Класс")
    male: bool = Field(description="Пол (мужчина или нет)")

    @field_validator("name", "surname")
    @staticmethod
    def name_validator(val):
        if " " in val:
            raise HTTPException(422, "name and surname should be one word")
        return val

    
class UserDTO(BaseUser):
    attachments: list[str] = Field(examples=[[f"{API_URL}/attachments/abcde1234567890"]], description="Вложения пользователя")
    verify: bool = Field(description="Верифицирован-ли пользователь")

    @field_validator("attachments", mode="before")
    @classmethod
    def attachments_refactor(cls, attachments: list[str] | list[Attachment]):
        if attachments and isinstance(attachments[0], Attachment):
            return [atch.url for atch in attachments]
        return attachments
    
class FriendUserDTO(UserDTO):
    username: str = Field(description="Username пользователя", examples=["exampleuser"])

class FullUserDTO(UserDTO):
    id: int = Field(description="ID пользователя", examples=[1000000000])
    is_active: bool = Field(description="Активна-ли анкета")
    focus_user: UserDTO | None = Field(description="Текущая просматриваемая анкета")
    focus_is_liked: bool = Field(description="Является-ли текущая анкета вашим ответом на лайк пользователя")

@partial_model
class PatchUser(BaseUser):
    is_active: bool = Field(description="Активна-ли анкета")

class ReportUser(BaseModel):
    reason: str = Field(min_length=3, max_length=64)

class UnbanUser(BaseModel):
    msg_id: int
    user_id: int

class BanUser(UnbanUser):
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
    success: bool
from pydantic import BaseModel, Field

from config import CLASS_LITERAL


class BaseUser(BaseModel):
    name: str = Field(max_length=64)
    surname: str = Field(max_length=64)
    desc: str = Field(max_length=128)
    literal: CLASS_LITERAL
    male: bool

class UserDTO(BaseUser):
    is_active: bool
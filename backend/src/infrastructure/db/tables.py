from sqlalchemy import BigInteger, Column, String
from sqlmodel import Field, Relationship, SQLModel, UUID

from config import API_URL, CLASS_LITERAL

class User(SQLModel, table = True):
    __tablename__ = "users"

    id: int = Field(sa_column=Column(BigInteger(), primary_key=True, autoincrement=False))
    name: str
    surname: str
    desc: str
    literal: CLASS_LITERAL = Field(sa_type=String)
    male: bool
    is_active: bool = Field(default=True)

    attachments: list["Attachment"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "selectin"})

class View(SQLModel, table = True):
    __tablename__ = "views"

    id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="users.id", index = True)
    target_id: int = Field(foreign_key="users.id")

class Like(SQLModel, table = True):
    __tablename__ = "likes"

    id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    target_id: int = Field(foreign_key="users.id")
    is_mutually: bool = Field(default=False)

class Attachment(SQLModel, table = True):
    __tablename__ = "attachments"

    id: str = Field(sa_type=String, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index = True)
    filetype: str

    user: User = Relationship(back_populates="attachments")

    @property
    def url(self) -> str:
        return API_URL + "/attachments/" + self.id
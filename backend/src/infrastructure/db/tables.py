from typing import Optional
from sqlalchemy import BigInteger, Column, String, false
from sqlmodel import Field, Relationship, SQLModel

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
    focus_id: int | None = Field(foreign_key="users.id")
    focus_is_liked: bool = Field(default=False, sa_column_kwargs={"server_default": false()})

    attachments: list["Attachment"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "selectin"})
    focus_user: Optional["User"] = Relationship(sa_relationship_kwargs={"remote_side": "User.id"})

class Action(SQLModel):

    id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="users.id", index = True)
    target_id: int = Field(foreign_key="users.id")

class View(Action, table = True):
    __tablename__ = "views"

class Like(Action, table = True):
    __tablename__ = "likes"

    is_mutually: bool = Field(default=False, sa_column_kwargs={"server_default": false()})
    user: User = Relationship(sa_relationship_kwargs={"foreign_keys": "Like.user_id"})
    target_user: User = Relationship(sa_relationship_kwargs={"foreign_keys": "Like.target_id"})

class Attachment(SQLModel, table = True):
    __tablename__ = "attachments"

    id: str = Field(sa_type=String, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index = True)
    filetype: str

    user: User = Relationship(back_populates="attachments")

    @property
    def url(self) -> str:
        return API_URL + "/attachments/" + self.id
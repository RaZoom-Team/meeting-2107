from datetime import datetime
from typing import Optional
from sqlalchemy import TIMESTAMP, BigInteger, Column, String, false, text, true
from sqlmodel import Field, Relationship, SQLModel

from config import API_URL, CLASS_LITERAL


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int = Field(sa_column=Column(
        BigInteger(),
        primary_key=True,
        autoincrement=False)
    )
    username: str
    name: str
    surname: str
    desc: str
    literal: CLASS_LITERAL = Field(sa_type=String)
    male: bool
    is_active: bool = Field(sa_column_kwargs={"server_default": true()})
    verify: bool = Field(sa_column_kwargs={"server_default": false()})
    focus_id: int | None = Field(
        sa_type=BigInteger(),
        foreign_key="users.id",
        ondelete="cascade"
    )
    focus_is_liked: bool = Field(sa_column_kwargs={"server_default": false()})
    is_banned: bool = Field(sa_column_kwargs={"server_default": false()})
    ban_reason: Optional[str]
    created_at: datetime = Field(sa_column=Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
    ))

    attachments: list["Attachment"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    focus_user: Optional["User"] = Relationship(
        sa_relationship_kwargs={"remote_side": "User.id"}
    )

    @property
    def mention(self) -> str:
        return self.custom_mention(self.fullname)

    def custom_mention(self, title: str) -> str:
        return f"<a href='t.me/{self.username}'>{title}</a>"

    @property
    def fullname(self) -> str:
        return f"{self.name} {self.surname}"


class Action(SQLModel):

    id: int = Field(primary_key=True)
    user_id: int = Field(
        sa_type=BigInteger(),
        foreign_key="users.id",
        index=True,
        ondelete="cascade"
    )
    target_id: int = Field(
        sa_type=BigInteger(),
        foreign_key="users.id",
        ondelete="cascade"
    )


class View(Action, table=True):
    __tablename__ = "views"


class Like(Action, table=True):
    __tablename__ = "likes"

    is_mutually: bool = Field(sa_column_kwargs={"server_default": false()})
    user: User = Relationship(sa_relationship_kwargs={
        "foreign_keys": "Like.user_id",
        "lazy": "selectin"
    })
    target_user: User = Relationship(sa_relationship_kwargs={
        "foreign_keys": "Like.target_id",
        "lazy": "selectin"
    })
    created_at: datetime = Field(sa_column=Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
    ))


class Attachment(SQLModel, table=True):
    __tablename__ = "attachments"

    id: str = Field(sa_type=String, primary_key=True)
    user_id: int = Field(
        sa_type=BigInteger(),
        foreign_key="users.id",
        index=True,
        ondelete="cascade"
    )
    filetype: str
    created_at: datetime = Field(sa_column=Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
    ))

    user: User = Relationship(back_populates="attachments")

    @property
    def url(self) -> str:
        return API_URL + "/attachments/" + self.id

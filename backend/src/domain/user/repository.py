from sqlalchemy import func
from sqlalchemy.orm import joinedload
from sqlmodel import desc, select
from config import CLASS_LITERAL
from infrastructure.db import BaseRepository, User, View, Like


class UserRepository(BaseRepository[User]):

    async def get(self, id: int) -> User | None:
        query = select(User).where(User.id == id).options(joinedload(User.focus_user))
        res = await self.session.exec(query)
        return res.first()
    
    async def get_all(self, offset: int, limit: int, filter = None) -> list[User]:
        query = select(User).offset(offset).limit(limit).order_by(desc(User.created_at)).filter(filter)
        res = await self.session.exec(query)
        return res.all()

    async def get_liked(self, user: User) -> User | None:
        query = select(User) \
        .join(Like, Like.user_id == User.id) \
        .filter((Like.target_id == user.id) & (Like.is_mutually == False) & User.is_active) \
        .limit(1)
        res = await self.session.exec(query)
        return res.first()

    async def get_noviewed(self, user: User) -> User | None:
        liked = await self.get_liked(user)
        if liked:
            user.focus_is_liked = True
            return liked
        query = select(User).where(
            (User.id != user.id) & (User.male != user.male) & User.is_active
            & (~User.id.in_(
                select(View.target_id).where(View.user_id == user.id).scalar_subquery()
            ))
            & (~User.id.in_(
                select(Like.target_id).where(Like.user_id == user.id).scalar_subquery()
            ))
        ) \
        .order_by(func.random()) \
        .limit(1)
        res = await self.session.exec(query)
        return res.first()

    async def insert(self, id: int, username: str, name: str, surname: str, male: bool, desc: str, literal: CLASS_LITERAL) -> User:
        user = User(
            id = id,
            username = username,
            name = name,
            surname = surname,
            male = male,
            desc = desc,
            literal = literal
        )
        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)
        return user
    
    async def count(self, filter = True) -> int:
        query = select(func.count()).select_from(User).filter(filter)
        res = await self.session.exec(query)
        return res.one()
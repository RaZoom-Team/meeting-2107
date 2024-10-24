from sqlalchemy import func
from sqlmodel import select, insert
from config import CLASS_LITERAL
from infrastructure.db import BaseRepository, User
from infrastructure.db.tables import View


class UserRepository(BaseRepository):

    async def get(self, id: int) -> User | None:
        query = select(User).where(User.id == id)
        res = await self.session.exec(query)
        return res.first()
    
    async def get_noviewed(self, user: User) -> User | None:
        query = select(User).where(
            (User.id != user.id) & (User.male != user.male) & ~User.id.in_(
                select(View.target_id).where(View.user_id == user.id).scalar_subquery()
            )
        ) \
        .order_by(func.random()) \
        .limit(1)
        res = await self.session.exec(query)
        return res.first()

    async def insert(self, id: int, name: str, surname: str, male: bool, desc: str, literal: CLASS_LITERAL) -> User:
        query = insert(User).values(
            id = id,
            name = name,
            surname = surname,
            male = male,
            desc = desc,
            literal = literal
        ).returning(User)
        res = await self.session.exec(query)
        return res.scalar_one()
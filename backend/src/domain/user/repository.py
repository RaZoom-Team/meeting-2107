from sqlalchemy import ChunkedIteratorResult
from sqlmodel import select, insert
from config import CLASS_LITERAL
from infrastructure.db import BaseRepository, User


class UserRepository(BaseRepository):

    async def get(self, id: int) -> User | None:
        query = select(User).where(User.id == id)
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
from sqlmodel import delete, insert

from infrastructure.db import BaseRepository, View, User

class ViewRepository(BaseRepository):

    async def drop_user(self, user: User) -> int:
        query = delete(View).where(View.user_id == user.id)
        res = await self.session.exec(query)
        return res.rowcount
    
    async def insert(self, user: User, target: User) -> View:
        query = insert(View).values(user_id = user.id, target_id = target.id).returning(View)
        res = await self.session.exec(query)
        return res.scalar_one()
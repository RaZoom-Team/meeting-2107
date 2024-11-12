from sqlmodel import delete, insert

from src.infrastructure.db import BaseRepository, View, User

class ViewRepository(BaseRepository[View]):

    async def drop_user(self, user: User) -> int:
        query = delete(View).where(View.user_id == user.id)
        res = await self.session.exec(query)
        return res.rowcount
    
    async def insert(self, user: User, target: User) -> View:
        view = View(
            user_id = user.id,
            target_id = target.id
        )
        self.session.add(view)
        await self.session.flush()
        await self.session.refresh(view)
        return view
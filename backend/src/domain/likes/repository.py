from sqlmodel import select, delete, insert

from infrastructure.db import BaseRepository, Like, User

class LikeRepository(BaseRepository):

    # async def drop_user(self, user: User) -> int:
    #     query = delete(View).where(View.user_id == user.id)
    #     res = await self.session.exec(query)
    #     return res.rowcount
    
    async def get_byuser(self, user: User, second_user: User) -> Like | None:
        query = select(Like).where(
            ((Like.user_id == user.id) & (Like.target_id == second_user.id))
            |
            ((Like.user_id == second_user.id) & (Like.target_id == user.id))
        )
        res = await self.session.exec(query)
        return res.first()
    
    async def get_mutually(self, user: User) -> list[User]:
        query = select(User).join_from(Like, Like.target_user).filter((Like.user_id == user.id) & (Like.is_mutually == True))
        res = await self.session.exec(query)
        return res.all()

    async def insert(self, user: User, target: User) -> Like:
        like = Like(
            user = user,
            target_user = target
        )
        self.session.add(like)
        await self.session.flush()
        await self.session.refresh(like)
        return like
    
    async def delete(self, like: Like) -> None:
        await self.session.delete(like)
        await self.session.flush()


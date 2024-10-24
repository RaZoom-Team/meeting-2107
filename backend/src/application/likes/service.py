from infrastructure.exc import FocusNotSelected
from infrastructure.db import Like, User
from application.user import UserService
from domain.likes import LikeRepository


class LikeService:
    
    def __init__(self) -> None:
        self.repo = LikeRepository()

    async def answer_focus(self, user: User, status: bool) -> None:
        if not user.focus_user:
            raise FocusNotSelected
        
        like = await self.repo.get_byuser(user, user.focus_user)
        if like:
            if like.target_user == user:
                await self.answer_like(like, status)
        else:
            if status:
                await self.repo.insert(user, user.focus_user)
        await UserService().select_focus(user)

    async def answer_like(self, like: Like, status: bool) -> None:
        if status:
            like.is_mutually = True
            like2 = await self.repo.insert(like.target_user, like.user)
            like2.is_mutually = True
        else:
            await self.repo.delete(like)

    async def get_all_mutually(self, user: User) -> list[User]:
        return await self.repo.get_mutually(user)
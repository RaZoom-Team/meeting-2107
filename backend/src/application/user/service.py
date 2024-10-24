from application.attachment import AttachmentService
from config import MAX_AVATAR_SIZE
from domain.user import BaseUser, UserRepository
from domain.views import ViewRepository
from infrastructure.db import User
from infrastructure.exc import AlreadyRegisteredException, FileSizeException


class UserService:

    def __init__(self) -> None:
        self.repo = UserRepository()

    async def register(self, user_id: int, data: BaseUser, avatar: bytes) -> User:
        if await self.repo.get(user_id):
            raise AlreadyRegisteredException
        if len(avatar) > MAX_AVATAR_SIZE:
            raise FileSizeException
        
        user = await self.repo.insert(
            id = user_id,
            name = data.name,
            surname = data.surname,
            desc = data.desc,
            literal = data.literal,
            male = data.male
        )
        await AttachmentService().upload(avatar, user)
        await self.select_focus(user)
        return user
    
    async def select_focus(self, user: User) -> User | None:
        if not user.is_active: return
        
        user.focus_user = None
        user.focus_is_liked = False
        focus = await self.repo.get_noviewed(user)
        if not focus:
            await ViewRepository().drop_user(user)
            focus = await self.repo.get_noviewed(user)
            if not focus: return
        await ViewRepository().insert(user, focus)
        user.focus_user = focus
        return focus
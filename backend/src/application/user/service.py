from application.attachment.service import AttachmentService
from config import MAX_AVATAR_SIZE
from domain.user import BaseUser, UserRepository
from infrastructure.db.tables import User
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
        await AttachmentService().upload(avatar, user_id)
        return user
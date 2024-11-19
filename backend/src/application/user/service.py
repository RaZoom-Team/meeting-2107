from src.application.attachment import AttachmentService
from src.application.tg import TelegramService
from src.config import MAX_AVATAR_SIZE
from src.domain.user import BaseUser, UserRepository
from src.domain.views import ViewRepository
from src.infrastructure.db import User
from src.infrastructure.exc.auth import UsernameRequired
from src.infrastructure.exc.likes import FocusNotSelected
from src.infrastructure.exc.user import AlreadyRegisteredException, AlreadyVerifiedException, FileSizeException, BannedException, SubscriptionRequiredException, VerifyRestrictionsException


class UserService:

    def __init__(self) -> None:
        self.repo = UserRepository()

    async def register(self, userdata: dict, data: BaseUser, avatar: bytes) -> User:
        if await self.repo.get(userdata['id']):
            raise AlreadyRegisteredException
        if not userdata.get("username", None):
            raise UsernameRequired
        if len(avatar) > MAX_AVATAR_SIZE:
            raise FileSizeException

        user = await self.repo.insert(
            id = userdata['id'],
            username = userdata['username'],
            name = data.name,
            surname = data.surname,
            desc = data.desc,
            literal = data.literal,
            male = data.male
        )
        await self.check_user_subcription(user)
        await AttachmentService().upload(avatar, user)
        await self.select_focus(user)
        await TelegramService().send_media_to_chat(
            "<b>👤 Новый пользователь</b>"
            f"\n<b>Имя:</b> {user.mention} <b>(<code>{user.id}</code>)</b>"
            f"\n<b>Класс:</b> {user.literal}"
            f"\n<b>Пол:</b> {'Мужской' if user.male else 'Женский'}"
            f"\n<b>Описание:</b> <i>{user.desc}</i>",
            [attachment.url for attachment in user.attachments]
        )
        return user

    async def select_focus(self, user: User) -> User | None:
        user.focus_user = None
        user.focus_is_liked = False
        if not user.is_active:
            return None
        focus = await self.repo.get_noviewed(user)
        if not focus:
            await ViewRepository().drop_user(user)
            focus = await self.repo.get_noviewed(user)
            if not focus:
                return
        await ViewRepository().insert(user, focus)
        user.focus_user = focus
        return focus
    
    async def send_verify_request(self, user: User) -> None:
        if user.verify:
            raise AlreadyVerifiedException()
        await TelegramService().send_media_to_chat(
            "<b>🔰 Новый запрос на верификацию</b>"
            f"\n<b>Имя:</b> {user.mention} <b>(<code>{user.id}</code>)</b>"
            f"\n<b>Класс:</b> {user.literal}"
            f"\n<b>Пол:</b> {'Мужской' if user.male else 'Женский'}"
            f"\n<b>Описание:</b> <i>{user.desc}</i>",
            [attachment.url for attachment in user.attachments]
        )

    async def update_avatar(self, user: User, avatar: bytes) -> None:
        if len(avatar) > MAX_AVATAR_SIZE:
            raise FileSizeException
        user.verify = False
        await AttachmentService().delete(user.attachments[0])
        await AttachmentService().upload(avatar, user)

    async def report_focus(self, user: User, reason: str) -> None:
        if not user.focus_user:
            raise FocusNotSelected
        target = user.focus_user
        await TelegramService().send_media_to_chat(
            "<b>🆘 Новый репорт</b>"
            f"\n<b>Отправитель:</b> {user.mention} <b>(<code>{user.id}</code>)</b>"
            f"\n<b>Нарушитель:</b> {target.mention} <b>(<code>{target.id}</code>)</b>"
            f"\n<b>Причина:</b> {reason}",
            [attachment.url for attachment in target.attachments]
        )
        await self.select_focus(user)

    async def edit_user(self, user: User, data: BaseUser) -> None:
        for field, value in data.model_dump().items():
            if value is not None and getattr(user, field) != value:
                if user.verify and field in [
                    "name",
                    "username",
                    "male",
                    "literal"
                ]:
                    user.verify = False
                setattr(user, field, value)
                if field in ["male", "is_active"]:
                    await self.select_focus(user)

    async def check_user(self, user: User, username: str) -> None:
        if not username:
            await self.set_active(user, False)
            raise UsernameRequired
        if user.username != username:
            user.username = username
        if not user.focus_user and user.is_active:
            await self.select_focus(user)
        if user.is_banned:
            await self.set_active(user, False)
            raise BannedException(user.ban_reason)
        
    async def check_user_subcription(self, user: User) -> None:
        if not await TelegramService().check_subscribed(user.id):
            await self.set_active(user, False)
            raise SubscriptionRequiredException
        
    async def ban(self, user: User, reason: str) -> None:
        user.is_banned = True
        user.ban_reason = reason
        await self.set_active(user, False)

    async def unban(self, user: User) -> None:
        user.is_banned = False
        user.ban_reason = None

    async def set_active(self, user: User, value: bool) -> None:
        user.is_active = value
        await self.select_focus(user)
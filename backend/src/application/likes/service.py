from application.tg.service import TelegramService
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
            if status and user.focus_user.is_active:
                await self.repo.insert(user, user.focus_user)
                await TelegramService().send_message(
                    "🥰 Твоя анкета кому-то понравилась"
                    "\n⚡️ Скорее заходи в приложение и посмотри кто это!",
                    user_id = user.focus_user.id
                )
        await UserService().select_focus(user)

    async def answer_like(self, like: Like, status: bool) -> None:
        if status:
            like.is_mutually = True
            like2 = await self.repo.insert(like.target_user, like.user)
            like2.is_mutually = True
            await TelegramService().send_message(
                f"❤️‍🔥 Ты взаимно лайкнул(-а) {like.user.fullname} из {like.user.literal}!"
                f"\n💬 Скорее переходите в {like.user.custom_mention("ЛС")} и общайтесь",
                user_id = like.target_user.id
            )
            await TelegramService().send_message(
                f"❤️‍🔥 {like.target_user.fullname} из {like.target_user.literal} взаимно лайкнул(-а) тебя!"
                f"\n💬 Скорее переходите в {like.target_user.custom_mention("ЛС")} и общайтесь",
                user_id = like.user.id
            )
        else:
            await self.repo.delete(like)

    async def get_all_mutually(self, user: User) -> list[User]:
        return await self.repo.get_mutually(user)

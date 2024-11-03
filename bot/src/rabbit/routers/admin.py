from faststream.rabbit import RabbitRouter

from config import TG_ADMIN_CHAT
from models import BannedUser, VerifiedUser
from telegram.bot import bot


router = RabbitRouter("adm_")

@router.subscriber("banned")
async def msg(ban: BannedUser) -> None:
    await bot.send_message(
        chat_id = TG_ADMIN_CHAT,
        reply_to_message_id = ban.msg_id,
        text = "🚫 Пользователь заблокирован" if ban.success else "❕ Неверный пользователь"
    )

@router.subscriber("verified")
async def msg(ban: VerifiedUser) -> None:
    await bot.send_message(
        chat_id = TG_ADMIN_CHAT,
        reply_to_message_id = ban.msg_id,
        text = "✅ Статус верификации пользователя обновлён" if ban.success else "❕ Неверный пользователь"
    )
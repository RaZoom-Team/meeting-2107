from faststream.rabbit import RabbitRouter
from aiogram.types import InputMediaPhoto, URLInputFile

from config import TG_ADMIN_CHAT
from models import BannedUser
from telegram.bot import bot


router = RabbitRouter("adm_")

@router.subscriber("banned")
async def msg(ban: BannedUser) -> None:
    await bot.send_message(
        chat_id = TG_ADMIN_CHAT,
        reply_to_message_id = ban.msg_id,
        text = "🚫 Пользователь заблокирован" if ban.success else "❕ Неверный пользователь"
    )
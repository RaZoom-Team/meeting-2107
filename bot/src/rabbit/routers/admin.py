from faststream.rabbit import RabbitRouter

from config import TG_ADMIN_CHAT
from models import TelegramRequestResponse
from models.admin import GetUserResponse
from telegram.bot import bot
from telegram.utlls import send_media


router = RabbitRouter("adm_")

@router.subscriber("banned")
async def msg(res: TelegramRequestResponse) -> None:
    await bot.send_message(
        chat_id = TG_ADMIN_CHAT,
        reply_to_message_id = res.msg_id,
        text = "🚫 Пользователь заблокирован" if res.success else "❕ Неверный пользователь"
    )

@router.subscriber("unbanned")
async def msg(res: TelegramRequestResponse) -> None:
    await bot.send_message(
        chat_id = TG_ADMIN_CHAT,
        reply_to_message_id = res.msg_id,
        text = "⛓️‍💥 Пользователь разблокирован" if res.success else "❕ Неверный пользователь"
    )

@router.subscriber("verified")
async def msg(res: TelegramRequestResponse) -> None:
    await bot.send_message(
        chat_id = TG_ADMIN_CHAT,
        reply_to_message_id = res.msg_id,
        text = "✅ Статус верификации пользователя обновлён" if res.success else "❕ Неверный пользователь"
    )

@router.subscriber("user-res")
async def msg(res: TelegramRequestResponse | GetUserResponse) -> None:
    await send_media(
        chat_id = TG_ADMIN_CHAT,
        text = res.text,
        parse_mode = "markdown",
        files = res.attachments
    )
from faststream.rabbit import RabbitRouter

from config import TG_ADMIN_CHAT
from models import TelegramRequestResponse
from models.admin import GetUserResponse
from telegram.bot import bot
from telegram.utlls import send_media


router = RabbitRouter("adm_")

@router.subscriber("banned")
async def banned(res: TelegramRequestResponse) -> None:
    await bot.send_message(
        chat_id = TG_ADMIN_CHAT,
        reply_to_message_id = res.msg_id,
        text = "🚫 Пользователь заблокирован" if res.success else "❕ Неверный пользователь"
    )

@router.subscriber("unbanned")
async def unbanned(res: TelegramRequestResponse) -> None:
    await bot.send_message(
        chat_id = TG_ADMIN_CHAT,
        reply_to_message_id = res.msg_id,
        text = "⛓️‍💥 Пользователь разблокирован" if res.success else "❕ Неверный пользователь"
    )

@router.subscriber("verified")
async def verified(res: TelegramRequestResponse) -> None:
    await bot.send_message(
        chat_id = TG_ADMIN_CHAT,
        reply_to_message_id = res.msg_id,
        text = "✅ Статус верификации пользователя обновлён" if res.success else "❕ Неверный пользователь"
    )

@router.subscriber("user-res")
async def get_user(res: GetUserResponse) -> None:
    if not res.success:
        return await bot.send_message(
            chat_id = TG_ADMIN_CHAT,
            reply_to_message_id = res.msg_id,
            text = "❕ Неверный пользователь"
        )
    await send_media(
        chat_id = TG_ADMIN_CHAT,
        text = res.text,
        files = res.attachments,
        reply_to = res.msg_id
    )
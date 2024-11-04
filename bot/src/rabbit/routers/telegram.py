from faststream.rabbit import RabbitRouter
from aiogram.types import InputMediaPhoto, URLInputFile

from config import TG_ADMIN_CHAT
from models import SendAdminMediaMessage, SendAdminMessage, SendMessage, SendMediaMessage
from telegram.bot import bot
from telegram.utlls import send_media


router = RabbitRouter("tg_")

@router.subscriber("msg")
async def sendmsg(msg: SendMessage | SendAdminMessage) -> None:
    try:
        await bot.send_message(
            chat_id = msg.chat_id if msg.chat_id != -1 else TG_ADMIN_CHAT,
            text = msg.text,
            parse_mode = msg.parse_mode
        )
    except: pass

@router.subscriber("media")
async def sendmedia(msg: SendMediaMessage | SendAdminMediaMessage) -> None:
    await send_media(
        chat_id = msg.chat_id if msg.chat_id != -1 else TG_ADMIN_CHAT,
        text = msg.text,
        parse_mode = msg.parse_mode,
        files = msg.files
    )


# @router.subscriber("report")
# async def send_report()
from aiogram import F, Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from config import TG_ADMIN_CHAT
from models.admin import BanUser
from rabbit.broker import broker

router = Router()

@router.message(Command("ban"), F.chat.id == TG_ADMIN_CHAT)
async def ban(msg: Message):
    args = msg.text.split()[1:]
    if len(args) < 2:
        return msg.reply("❕ Use: /ban [USER_ID] [REASON]")
    user_id, reason = args[0], ' '.join(args[1:])
    await broker.publish(
        BanUser(msg_id = msg.message_id, user_id = user_id, reason = reason),
        "adm_ban"
    )
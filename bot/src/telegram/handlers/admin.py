from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from config import TG_ADMIN_CHAT
from models.admin import BanUser, GetUser, UnbanUser, VerifyUser
from rabbit.broker import broker

handler = Router()

@handler.message(Command("ban"), F.chat.id == TG_ADMIN_CHAT)
async def ban(msg: Message):
    args = msg.text.split()[1:]
    if len(args) < 2 or not args[0].isdigit():
        return msg.reply("❕ Use: /ban [USER_ID] [REASON]")
    user_id, reason = args[0], ' '.join(args[1:])
    await broker.publish(
        BanUser(msg_id = msg.message_id, user_id = user_id, reason = reason),
        "adm_ban"
    )

@handler.message(Command("unban"), F.chat.id == TG_ADMIN_CHAT)
async def ban(msg: Message):
    args = msg.text.split()[1:]
    if len(args) < 1 or not args[0].isdigit():
        return msg.reply("❕ Use: /unban [USER_ID]")
    await broker.publish(
        UnbanUser(msg_id = msg.message_id, user_id = args[0]),
        "adm_unban"
    )

@handler.message(Command("verify"), F.chat.id == TG_ADMIN_CHAT)
async def ban(msg: Message):
    args = msg.text.split()[1:]
    if len(args) < 1 or not args[0].isdigit():
        return msg.reply("❕ Use: /verify [USER_ID]")
    await broker.publish(
        VerifyUser(msg_id = msg.message_id, user_id = args[0], value = True),
        "adm_verify"
    )

@handler.message(Command("denyverify"), F.chat.id == TG_ADMIN_CHAT)
async def ban(msg: Message):
    args = msg.text.split()[1:]
    if len(args) < 2 or not args[0].isdigit():
        return msg.reply("❕ Use: /denyverify [USER_ID] [REASON]")
    user_id, reason = args[0], ' '.join(args[1:])
    try:
        await msg.bot.send_message(
            chat_id = user_id,
            text = f"⛔️ Вам отказано в верификации\n{reason}"
        )
        await msg.reply("✅ В верификации отказано")
    except:
        await msg.reply("❗️ Сообщение не было доставлено")

@handler.message(Command("unverify"), F.chat.id == TG_ADMIN_CHAT)
async def ban(msg: Message):
    args = msg.text.split()[1:]
    if len(args) < 1 or not args[0].isdigit():
        return msg.reply("❕ Use: /unverify [USER_ID]")
    await broker.publish(
        VerifyUser(msg_id = msg.message_id, user_id = args[0], value = False),
        "adm_verify"
    )

@handler.message(Command("get"), F.chat.id == TG_ADMIN_CHAT)
async def ban(msg: Message):
    args = msg.text.split()[1:]
    if len(args) < 1 or not args[0].isdigit():
        return msg.reply("❕ Use: /get [USER_ID]")
    await broker.publish(
        GetUser(msg_id = msg.message_id, user_id = args[0]),
        "adm_user"
    )
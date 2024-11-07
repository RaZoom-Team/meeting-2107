from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from application.rabbit.messages import ban_user, get_users, unban_user, get_user, verify_user
from infrastructure.telegram import Data, send_media
from infrastructure.telegram.keyboards import create_users_keyboard
from models.admin import ReasonRequest, UserRequest
from config import TG_ADMIN_CHAT

handler = Router()

USERS_LIST_LIMIT = 25

@handler.message(Command("ban"), F.chat.id == TG_ADMIN_CHAT)
async def ban(
    msg: Message,
    data: ReasonRequest = Data(["user_id", ":reason"], "❕ Use: /ban [USER_ID] [REASON]")
):
    res = await ban_user(data.user_id, data.reason)
    if not res.success:
        return await msg.reply(f"❕ {res.error}")
    await msg.reply("🚫 Пользователь заблокирован")

@handler.message(Command("unban"), F.chat.id == TG_ADMIN_CHAT)
async def unban(
    msg: Message,
    data: UserRequest = Data(["user_id"], "❕ Use: /unban [USER_ID]")
):
    res = await unban_user(data.user_id)
    if not res.success:
        return await msg.reply(f"❕ {res.error}")
    await msg.reply("⛓️‍💥 Пользователь разблокирован")

@handler.message(Command("verify"), F.chat.id == TG_ADMIN_CHAT)
async def verify(
    msg: Message,
    data: UserRequest = Data(["user_id"], "❕ Use: /verify [USER_ID]")
):
    res = await verify_user(data.user_id, True)
    if not res.success:
        return await msg.reply(f"❕ {res.error}")
    await msg.reply("✅ Пользователь был верифицирован")

@handler.message(Command("unverify"), F.chat.id == TG_ADMIN_CHAT)
async def unverify(
    msg: Message,
    data: UserRequest = Data(["user_id"], "❕ Use: /unverify [USER_ID]")
):
    res = await verify_user(data.user_id, False)
    if not res.success:
        return await msg.reply(f"❕ {res.error}")
    await msg.reply("✅ Верификация пользователя была снята")

@handler.message(Command("denyverify"), F.chat.id == TG_ADMIN_CHAT)
async def denyverify(
    msg: Message,
    data: ReasonRequest = Data(["user_id", ":reason"], "❕ Use: /denyverify [USER_ID] [REASON]")
):
    try:
        await msg.bot.send_message(
            chat_id = data.user_id,
            text = f"🚫 Вам отказано в верификации по причине:\n<i>{data.reason}</i>",
            parse_mode = "html"
        )
        await msg.reply("✅ Отказ был доставлен пользователю")
    except Exception as err:
        print(err)
        await msg.reply("❕ Не удалось доставить отказ пользователю")

@handler.message(Command("get"), F.chat.id == TG_ADMIN_CHAT)
async def user(
    msg: Message,
    data: UserRequest = Data(["user_id"], "❕ Use: /get [USER_ID]")
):
    res = await get_user(data.user_id)
    if not res.success:
        return await msg.reply(f"❕ {res.error}")
    await send_media(
        msg.chat.id,
        res.response.text,
        res.response.attachments,
        msg.message_id
    )

@handler.message(Command("users"), F.chat.id == TG_ADMIN_CHAT)
async def user(msg: Message, state: FSMContext):
    res = await get_users(0, USERS_LIST_LIMIT)
    if not res.success:
        return await msg.reply(f"❕ {res.error}")
    answer = await msg.reply(
        res.response.text,
        link_preview_options={"is_disabled": True},
        reply_markup=create_users_keyboard(0, res.response.count % USERS_LIST_LIMIT != 0)
    )
    await state.update_data(**{f"users_{answer.message_id}": {"offset": 0}}, test = 1)

@handler.callback_query(F.data.in_(["users_next", "users_back"]))
async def user_scroll(query: CallbackQuery, state: FSMContext):
    key = f"users_{query.message.message_id}"
    data = await state.get_value(key)
    data['offset'] += USERS_LIST_LIMIT if query.data == "users_next" else -USERS_LIST_LIMIT
    res = await get_users(data['offset'], USERS_LIST_LIMIT)
    await state.update_data(**{key: data})
    if res.success:
        await query.message.edit_text(
            res.response.text,
            link_preview_options={"is_disabled": True},
            reply_markup=create_users_keyboard(data['offset'], res.response.count % USERS_LIST_LIMIT != 0)
        )
    await query.answer(None)
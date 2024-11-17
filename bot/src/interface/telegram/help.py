from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command


handler = Router()

@handler.message(Command("help"))
async def help(msg: Message):
    await msg.reply(
        "❔ Список команд"
        "\n<b>/ban</b> - Блокировка пользователя"
        "\n<b>/unban</b> - Разблокировки пользователя"
        "\n<b>/verify</b> - Верификация пользователя"
        "\n<b>/unverify</b> - Отзыв верификации пользователя"
        "\n<b>/denyverify</b> - Отказ в верификации пользователю"
        "\n<b>/warn</b> - Уведомление пользователю"
        "\n<b>/get</b> - Получение информации о пользователе"
        "\n<b>/users</b> - Список пользователей"
    )
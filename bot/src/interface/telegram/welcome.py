from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart


handler = Router()

@handler.message(CommandStart())
async def help(msg: Message):
    await msg.reply("Добро пожаловать в Дайвинчик 2107, для перехода в приложение нажмите на кнопку Open внизу слева.")
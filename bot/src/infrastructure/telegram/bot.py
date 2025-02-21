from aiogram import Bot
from aiogram.types import InputMediaPhoto, URLInputFile
from aiogram.client.bot import DefaultBotProperties
from aiogram.fsm.strategy import FSMStrategy

from config import TG_TOKEN

bot = Bot(TG_TOKEN, default = DefaultBotProperties(parse_mode='html'), fsm_strategy = FSMStrategy)

async def send_media(chat_id: int, text: str, files: list[str], reply_to: int = None, parse_mode: str = "html") -> None:
    await bot.send_media_group(
        chat_id = chat_id,
        media = [
            InputMediaPhoto(
                media = URLInputFile(file),
                caption = text if i == 0 else None,
                parse_mode = parse_mode
            )
            for i, file in enumerate(files)
        ],
        reply_to_message_id = reply_to
    )
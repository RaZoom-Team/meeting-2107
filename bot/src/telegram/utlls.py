from aiogram.types import InputMediaPhoto, URLInputFile

from .bot import bot


async def send_media(chat_id: int, text: str, files: list[str], parse_mode: str = "html") -> None:
    await bot.send_media_group(
        chat_id = chat_id,
        media = [
            InputMediaPhoto(
                media = URLInputFile(file),
                caption = text if i == 0 else None,
                parse_mode = parse_mode
            )
            for i, file in enumerate(files)
        ]
    )
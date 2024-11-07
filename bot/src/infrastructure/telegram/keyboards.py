from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def create_users_keyboard(offset: int, end: bool) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[
        *([InlineKeyboardButton(text="Назад", callback_data="users_back")] if offset > 0 else []),
        *([InlineKeyboardButton(text="Дальше", callback_data="users_next")] if not end else []),
    ]])
    return keyboard
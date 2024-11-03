from aiogram import Dispatcher

from .handlers import AdminHandler


dp = Dispatcher()
dp.include_router(AdminHandler)
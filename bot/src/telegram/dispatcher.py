from aiogram import Dispatcher

from .handlers import AdminRouter


dp = Dispatcher()
dp.include_router(AdminRouter)
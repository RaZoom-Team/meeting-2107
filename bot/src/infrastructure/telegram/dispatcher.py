from aiogram import Dispatcher

from .validating_middleware import ValidatingMiddleware


dp = Dispatcher()
dp.message.middleware(ValidatingMiddleware())
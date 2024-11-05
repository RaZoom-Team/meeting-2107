from faststream.rabbit.fastapi import RabbitRouter

from config import RABBIT_URL
from .middlewares import DatabaseMiddleware, exc_middlware


rabbit = RabbitRouter(RABBIT_URL, include_in_schema=False, middlewares=[DatabaseMiddleware, exc_middlware])
broker = rabbit.broker
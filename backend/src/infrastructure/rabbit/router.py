from faststream.rabbit.fastapi import RabbitRouter

from config import RABBIT_URL
from .middlewares import DatabaseMiddleware


rabbit = RabbitRouter(RABBIT_URL, include_in_schema=False, middlewares=[DatabaseMiddleware])
broker = rabbit.broker
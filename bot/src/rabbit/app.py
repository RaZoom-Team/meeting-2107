from faststream import FastStream
from .broker import broker
from .routers import TelegramRouter, AdminRouter

app = FastStream(broker)
broker.include_routers(TelegramRouter, AdminRouter)
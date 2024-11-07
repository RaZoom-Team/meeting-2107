import traceback
from typing import Any
from faststream import BaseMiddleware, ExceptionMiddleware

from domain.user.models import RabbitRequestResponse
from infrastructure.db import CTX_SESSION, get_session

class DatabaseMiddleware(BaseMiddleware):
    async def on_receive(self):
        CTX_SESSION.set(get_session())
        return await super().on_receive()

    async def after_processed(self, exc_type, exc_val, exc_tb):
        await CTX_SESSION.get().close()
        return await super().after_processed(exc_type, exc_val, exc_tb)
    
class RabbitError(Exception):
    def __init__(self, body: Any) -> None:
        self.body = body

exc_middlware = ExceptionMiddleware()

@exc_middlware.add_handler(RabbitError, publish=True)
def rabbit_error(exc: RabbitError):
    return exc.body

@exc_middlware.add_handler(Exception, publish=True)
def rabbit_error(exc: Exception):
    traceback.print_exception(exc)
    return RabbitRequestResponse(success = False, error = "Internal error")

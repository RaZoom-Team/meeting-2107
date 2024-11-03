from faststream import BaseMiddleware

from infrastructure.db import CTX_SESSION, get_session

class DatabaseMiddleware(BaseMiddleware):
    async def on_receive(self):
        CTX_SESSION.set(get_session())
        return await super().on_receive()

    async def after_processed(self, exc_type, exc_val, exc_tb):
        await CTX_SESSION.get().close()
        return await super().after_processed(exc_type, exc_val, exc_tb)
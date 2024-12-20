import asyncio
import logging
from infrastructure.telegram import dp, bot
from infrastructure.rabbit import app
from interface.telegram import AdminHandler, HelpHandler, WelcomeHandler
from interface.rabbit import TelegramRouter

logging.basicConfig(level=logging.INFO)
dp.include_routers(AdminHandler, HelpHandler, WelcomeHandler)

app.broker.include_router(TelegramRouter)

@app.after_startup
async def run_dp():
    asyncio.create_task(dp.start_polling(bot))
app.on_shutdown(dp.stop_polling)
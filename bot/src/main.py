import asyncio
import logging
from rabbit.app import app
from telegram.dispatcher import dp
from telegram.bot import bot

logging.basicConfig(level=logging.INFO)

async def run():
    asyncio.ensure_future(dp.start_polling(bot))
    await app.run()

asyncio.run(run())
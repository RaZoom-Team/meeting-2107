import asyncio
import logging
from rabbit.app import app
from telegram.dispatcher import dp
from telegram.bot import bot

logging.basicConfig(level=logging.INFO)

async def main():
    await asyncio.gather(app.run(), dp.start_polling(bot))

if __name__ == "__main__":
    asyncio.run(main())
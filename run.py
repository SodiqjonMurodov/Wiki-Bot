import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from app.handlers import router
import wikipedia
from dotenv import load_dotenv

# load .env file
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def main():
    dp.include_router(router)
    await wikipedia.set_lang("ru")
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO) # logging
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')


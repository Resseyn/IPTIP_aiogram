import asyncio
import logging
import sys
import threading

from aiogram import Bot
from aiogram.enums import ParseMode
from loader import TOKEN
from handlers import dp


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

    asyncio.run(main())

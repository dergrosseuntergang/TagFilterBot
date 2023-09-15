import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from tortoise import Tortoise
from config import db_url

from config import TOKEN
import handlers


async def db_init():
    await Tortoise.init(
        db_url=db_url,
        modules={'models': ['models']}
    )
    await Tortoise.generate_schemas()


async def bot_init() -> None:
    mybot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_routers(handlers.router, handlers.cp_router)
    await dp.start_polling(mybot)


async def main() -> None:
    task1 = asyncio.create_task(db_init())
    task2 = asyncio.create_task(bot_init())

    await task1
    await task2

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

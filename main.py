import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from config.config import database, TOKEN
from routers.handlers import main_router

dp = Dispatcher()


async def on_startup(dispatcher: Dispatcher, bot: Bot):
    database['users'] = database.get('users', {})
    database['messages'] = database.get('messages', [])
    command_list = [
        BotCommand(command='start', description='Botni boshlash'),
        BotCommand(command='msg', description='habarlar sonini kurish'),
    ]
    await bot.set_my_commands(command_list)


async def on_shutdown(dispatcher: Dispatcher, bot: Bot):
    await bot.delete_my_commands()


async def main() -> None:
    bot = Bot(token=TOKEN)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.include_router(
        main_router,
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

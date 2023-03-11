import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand, BotCommandScopeAllGroupChats

from config import BOT_TOKEN
from handlers import register_router

logger = logging.getLogger(__name__)

bot_commands = (
    ('anime', 'Найти аниме к прикрепленному фото (reply)'),
)
commands_for_bot = []

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")

    storage = MemoryStorage()
    bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
    dp = Dispatcher(storage=storage)

    for cmd in bot_commands:
        commands_for_bot.append(BotCommand(command=cmd[0], description=cmd[1]))
    await bot.set_my_commands(commands=commands_for_bot,scope=BotCommandScopeAllGroupChats())

    register_router(dp)

    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Бот був вимкнений!")

from aiogram import Router
from aiogram.filters import CommandStart

from handlers.message import search
from handlers.start import start


def register_router(router: Router):
    router.message.register(start,CommandStart())
    router.message.register(search)
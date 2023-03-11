from aiogram import Router, F
from aiogram.filters import CommandStart, Command

from handlers.message import search, searchInGroup
from handlers.start import start


def register_router(router: Router):
    router.message.register(start,CommandStart(),F.chat.type == "private")
    router.message.register(search,F.chat.type == "private")
    router.message.register(searchInGroup,Command(commands=['anime']))
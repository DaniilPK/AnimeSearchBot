import html

from aiogram import types


async def start(message: types.Message):
    await message.answer(f'Отправьте любой фрагмент из аниме что бы узнать его название')
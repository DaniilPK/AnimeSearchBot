from aiogram import types


async def start(message: types.Message):
    await message.answer(f'Отправьте любую фотографию из аниме что бы узнать его название')

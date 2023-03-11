import logging
from aiogram import types, Bot
from aiogram.exceptions import TelegramBadRequest
from saucenaopie.helper import SauceIndex
from saucenaopie.exceptions import UnknownServerError
from config import client


async def search(message: types.Message, bot: Bot):
    await bot.send_chat_action(message.chat.id, action='typing')
    if message.photo or message.sticker:
        if message.sticker:
            res = await bot.get_file(message.sticker.file_id)
        else:
            res = await bot.get_file(message.photo[-1].file_id)

        photo = await bot.download_file(res.file_path)

        try:
            sauce = client.search(photo, result_limit=5,index=SauceIndex.ANIME and SauceIndex.H_ANIME)
        except UnknownServerError:
            return message.answer('Ошибка сервера')
        del photo
        Found = True
        try:
            for result in sauce.results:
                print(result.index, result.index.id, result.similarity, result.data)
                if result.index.id == 21:
                    Found = False
                    if result.data.urls:
                        try:
                            await message.answer_photo(result.data.urls[-1],
                                                       caption=f'{result.index} <b>{result.data.title}</b>\n'
                                                               f'Similarity: {result.similarity}%\n'
                                                               f'Episode:{result.data.episode} Timestamp: {result.data.timestamp}')
                        except TelegramBadRequest:
                            await message.answer(f'{result.index} <b>{result.data.title}</b>\n'
                                                 f'Similarity: {result.similarity}%\n'
                                                 f'Episode:{result.data.episode} Timestamp: {result.data.timestamp}')
                    else:
                        await message.answer(f'{result.index} <b>{result.data.title}</b>\n'
                                             f'Similarity: {result.similarity}%\n'
                                             f'Episode:{result.data.episode} Timestamp: {result.data.timestamp}')
                    break
                elif result.index.id == 22:
                    Found = False
                    await message.answer(f'{result.index} <b>{result.data.title}</b>\n'
                                             f'Similarity: {result.similarity}%\n'
                                             f'Episode:{result.data.episode} Timestamp: {result.data.timestamp}')
                    break
            if Found:
                await message.answer('Аниме не найдено')
        except Exception as ex:
            logging.error(ex)


async def searchInGroup(message: types.Message, bot: Bot):
    await bot.send_chat_action(message.chat.id,action='typing')
    if message.reply_to_message:
        if message.reply_to_message.photo or message.reply_to_message.sticker:
            if message.reply_to_message.photo or message.reply_to_message.sticker:
                if message.reply_to_message.sticker:
                    res = await bot.get_file(message.reply_to_message.sticker.file_id)
                else:
                    res = await bot.get_file(message.reply_to_message.photo[-1].file_id)

                photo = await bot.download_file(res.file_path)
                try:
                    sauce = client.search(photo, result_limit=5,index=SauceIndex.ANIME and SauceIndex.H_ANIME)
                except UnknownServerError:
                    return message.answer('Ошибка сервера')
                del photo
                Found = True
                try:
                    for result in sauce.results:
                        print(result.index, result.similarity, result.data)
                        if result.index.id == 21:
                            Found = False
                            if result.data.urls:
                                try:
                                    await message.reply_photo(result.data.urls[-1],
                                                              caption=f'{result.index} <b>{result.data.title}</b>\n'
                                                                      f'Similarity: {result.similarity}%\n'
                                                                      f'Episode:{result.data.episode} Timestamp: {result.data.timestamp}')
                                except TelegramBadRequest:
                                    await message.reply(f'{result.index} <b>{result.data.title}</b>\n'
                                                        f'Similarity: {result.similarity}%\n'
                                                        f'Episode:{result.data.episode} Timestamp: {result.data.timestamp}')
                            else:
                                await message.reply(f'{result.index} <b>{result.data.title}</b>\n'
                                                    f'Similarity: {result.similarity}%\n'
                                                    f'Episode:{result.data.episode} Timestamp: {result.data.timestamp}')
                            break
                        elif result.index.id == 22:
                            Found = False
                            await message.reply(f'{result.index} <b>{result.data.title}</b>\n'
                                                    f'Similarity: {result.similarity}%\n'
                                                    f'Episode:{result.data.episode} Timestamp: {result.data.timestamp}')
                    if Found:
                        await message.reply('Аниме не найдено')
                except Exception as ex:
                    logging.error(ex)
        else:
            await message.answer('фото или стикер не найден.')
    else:
        await message.answer('Не найдено прикрепленное сообщение ( reply ) .')

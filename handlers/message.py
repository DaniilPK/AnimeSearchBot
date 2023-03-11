import logging
from aiogram import types, Bot
from config import client


async def search(message: types.Message, bot: Bot):
    if message.photo or message.sticker:
        if message.sticker:
            res = await bot.get_file(message.sticker.file_id)
        else:
            res = await bot.get_file(message.photo[-1].file_id)

        photo = await bot.download_file(res.file_path)

        sauce = client.search(photo, result_limit=5)

        try:
            for result in sauce.results:
                print(result.index, result.similarity, result.data)
                if result.index.id == 21:
                    if result.data.urls:
                        await message.answer_photo(result.data.urls[-1],
                                                   caption=f'{result.index} <b>{result.data.title}</b>\n'
                                                           f'Similarity: {result.similarity}%\n'
                                                           f'Episode:{result.data.episode} Timestamp: {result.data.timestamp}')
        except Exception as ex:
            logging.error(ex)


async def searchInGroup(message: types.Message, bot: Bot):
    if message.reply_to_message:
        if message.reply_to_message.photo or message.reply_to_message.sticker:
            if message.reply_to_message.photo or message.reply_to_message.sticker:
                if message.reply_to_message.sticker:
                    res = await bot.get_file(message.reply_to_message.sticker.file_id)
                else:
                    res = await bot.get_file(message.reply_to_message.photo[-1].file_id)

                photo = await bot.download_file(res.file_path)
                sauce = client.search(photo, result_limit=5)

                try:
                    for result in sauce.results:
                        print(result.index, result.similarity, result.data)
                        if result.index.id == 21:
                            if result.data.urls:
                                await message.reply_photo(result.data.urls[-1],
                                                          caption=f'{result.index} <b>{result.data.title}</b>\n'
                                                                  f'Similarity: {result.similarity}%\n'
                                                                  f'Episode:{result.data.episode} Timestamp: {result.data.timestamp}')
                except Exception as ex:
                    logging.error(ex)
        else:
            await message.answer('фото или стикер не найден.')
    else:
        await message.answer('Не найдено прикрепленное сообщение ( reply ) .')

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import gsheet
import get_goods
from cfg import bot_token
from bot import keyboards

# Bot init
bot = Bot(token=bot_token.token)
dp = Dispatcher(bot)


# Bot start screen
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    user_data = await message.answer('Чтобы обновить прайс, используй кнопки ниже',
                                     reply_markup=keyboards.start_screen_kb)
    print(user_data)


# Commands from keyboard handler
@dp.message_handler()
async def text_commands_handler(message: types.Message):
    if message.text == 'Обновить прайс 📃':
        await message.answer('Обновление началось')
        get_goods.get_items()
        gsheet.sheet_upload()
        await message.answer('Выгружен список товаров🫡\n'
                             'Таблица обновлена✅')

    elif message.text == 'Обновить наценки 💸':
        await message.answer('Функция в разработке🚧')


if __name__ == '__main__':
    executor.start_polling(dp)

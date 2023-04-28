from aiogram import types
from aiogram.dispatcher.filters import Text

from Markups import balance_markup
from Markups import customer_menu_markup
from Markups import executor_menu_markup
from main import BotDB
from main import bot
from main import dp


@dp.message_handler(Text(equals="Перейти в меню исполнителя"))
async def menu_executor(message: types.Message):
    await bot.send_message(message.chat.id, "Меню", reply_markup=executor_menu_markup)


@dp.message_handler(Text(equals="Перейти в меню заказчика"))
async def menu_customer(message: types.Message):
    await bot.send_message(message.chat.id, "Меню", reply_markup=customer_menu_markup)

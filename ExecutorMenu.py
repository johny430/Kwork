from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from main import bot
from main import dp


class OrderForm(StatesGroup):
    Name = State()
    Price = State()
    Description = State()


@dp.message_handler(Text(equals="Разместить заказ"))
async def order_place(message: types.Message):
    await bot.send_message(message.chat.id, "Введите название заказа:", reply_markup=markup)
    await OrderForm.Name.set()

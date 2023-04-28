from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State

from Markups import balance_markup
from Markups import customer_menu_markup
from main import Database
from main import bot
from main import dp


class BalanceForm(StatesGroup):
    Check = State()
    Amount = State()
    Confirm = State()


@dp.message_handler(Text(equals="Баланс"))
async def check_balance(message: types.Message):
    money = Database.get_balance(user_id=message.from_user.id)
    await bot.send_message(message.chat.id, 'Ваш балланс = ' + str(money) + " Баллов", reply_markup=balance_markup)
    await BalanceForm.Check.set()


@dp.message_handler(state=BalanceForm.Check)
async def change_balance(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await bot.send_message(message.chat.id, "Меню:", reply_markup=customer_menu_markup)
        await state.finish()
    elif message.text == "Пополнить баланс":
        await bot.send_message(message.chat.id, "Введите количество:", reply_markup=customer_menu_markup)
        await state.finish()
    else:
        await bot.send_message(message.chat.id, "Меню:", reply_markup=customer_menu_markup)
        await state.finish()

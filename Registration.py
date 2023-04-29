import enum

import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from Markups import customer_menu_markup
from Markups import executor_menu_markup
from Markups import registration_markup
from main import Database
from main import bot
from main import dp


class RegistrationType(enum.IntEnum):
    as_executor = 1
    as_customer = 2


class Executor(StatesGroup):
    Type = State()
    INN = State()
    Fio = State()
    BirthDate = State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if Database.user_exists(message.from_user.id):
        await bot.send_message(message.chat.id, "Выберите пункт меню", reply_markup=customer_menu_markup)
    else:
        Database.add_user(message.from_user.id, 0)
        await message.answer("Здравствуйте, " + message.from_user.first_name + "!\nСпасибо за регистрацию на бирже!", reply_markup=customer_menu_markup)


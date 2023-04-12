import enum

import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from Markups import customer_menu_markup
from Markups import executor_menu_markup
from Markups import registration_markup
from main import BotDB
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
    if BotDB.user_exists(message.from_user.id):
        await bot.send_message(message.chat.id, "Выберите пункт меню", reply_markup=customer_menu_markup)
    else:
        await Executor.Type.set()
        await message.answer("Здравствуйте, выберите тип регистрации", reply_markup=registration_markup)


@dp.message_handler(state=Executor.Type)
async def executor1(message: types.Message, state: FSMContext):
    if message.text == "Зарегистрироваться как заказчик":
        async with state.proxy() as data_storage:
            data_storage["type"] = RegistrationType.as_customer
        await message.answer("Введите ваш ИНН для проверки")
        await Executor.INN.set()
    elif message.text == "Зарегистрироваться как исполнитель":
        async with state.proxy() as data_storage:
            data_storage["type"] = RegistrationType.as_executor
        await message.answer("Введите ваш ИНН для проверки")
        await Executor.INN.set()
    else:
        await bot.send_message(message.chat.id, "Выбериет тип регистрации!", reply_markup=registration_markup)


@dp.message_handler(state=Executor.INN)
async def executor2(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        inn = message.text
        response = requests.get(f'https://api-fns.ru/api/egr?req={inn}&key=80941fa261868b22d216aa0bfab4c226304b36f6')
        if response.status_code == 200 and len(response.json()['items']) != 0:
            await bot.send_message(message.chat.id, f'Ваш ИНН: {inn}')
            async with state.proxy() as data_storage:
                data_storage["inn"] = inn
            await bot.send_message(message.chat.id, "Введите Фио")
            await Executor.Fio.set()
        else:
            await bot.send_message(message.chat.id, 'Пользователь с таким ИНН не найден.')
    else:
        await bot.send_message(message.chat.id, "Введите корректный ИНН")


@dp.message_handler(state=Executor.Fio)
async def executor3(message: types.Message, state: FSMContext):
    fio = message.text.split(" ")
    if len(fio) == 3:
        async with state.proxy() as data_storage:
            data_storage["last_name"] = str(fio[0])
            data_storage["first_name"] = str(fio[1])
            data_storage["surname"] = str(fio[2])
        await bot.send_message(message.chat.id, "Введите дату рождения в формате чч.мм.гг")
        await Executor.BirthDate.set()
    else:
        await bot.send_message(message.chat.id, "Введите корректное фио")


def valid(birth_date):
    return birth_date[0].isdigit() and birth_date[1].isdigit() and birth_date[2].isdigit() and int(
        birth_date[0]) <= 31 and int(birth_date[1]) <= 12 and int(birth_date[2]) <= 2023


@dp.message_handler(state=Executor.BirthDate)
async def executor4(message: types.Message, state: FSMContext):
    birth_date = message.text.split(".")
    if len(birth_date) == 3 and valid(birth_date):
        async with state.proxy() as data_storage:
            first_name = data_storage["first_name"]
            last_name = data_storage["last_name"]
            surname = data_storage["surname"]
            inn = data_storage["inn"]
            account_type = data_storage["type"]
            markup = executor_menu_markup if account_type == RegistrationType.as_executor else customer_menu_markup
            BotDB.add_user(int(inn), str(first_name), str(last_name), str(surname), str(message.text),
                           int(message.from_user.id), int(account_type))
            await state.finish()
            profile = f'{last_name}\n{first_name}\n{surname}\n{inn}\n{message.text}'
            await bot.send_message(message.chat.id, "Регистрация прошла успешно!\nВаши данные:\n" + profile,
                                   reply_markup=markup)
    else:
        await bot.send_message(message.chat.id, "Введите корректную дату рождения в формате чч.мм.гг")

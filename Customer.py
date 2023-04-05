from main import dp
from main import bot
from main import BotDB
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram import types
import requests
class Customer(StatesGroup):
    INN = State()
    Fio = State()
    BirthDate = State()


@dp.message_handler(Text(equals="Зарегистрироваться как заказчик"))
async def Customer1(message: types.Message):
    await message.answer("Введите ваш ИНН для проверки")
    await Customer.INN.set()

@dp.message_handler(state=Customer.INN)
async def Customer2(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        inn = message.text
        response = requests.get(f'https://api-fns.ru/api/egr?req={inn}&key=80941fa261868b22d216aa0bfab4c226304b36f6')
        if response.status_code == 200 and len(response.json()['items']) != 0:
            await bot.send_message(message.chat.id, f'Ваш ИНН: {inn}')
            async with state.proxy() as data_storage:
                data_storage["inn"] = inn
            await bot.send_message(message.chat.id, "Введите Фио")
            await Customer.Fio.set()
        else:
            await bot.send_message(message.chat.id, 'Пользователь с таким ИНН не найден.')
    else:
        await bot.send_message(message.chat.id, "Введите корректный ИНН")


@dp.message_handler(state=Customer.Fio)
async def Customer3(message: types.Message, state: FSMContext):
    fio = message.text.split(" ")
    if len(fio) == 3:
        async with state.proxy() as data_storage:
            data_storage["last_name"] = str(fio[0])
            data_storage["first_name"] = str(fio[1])
            data_storage["surname"] = str(fio[2])
        await bot.send_message(message.chat.id, "Введите дату рождения в формате чч.мм.гг")
        await Customer.BirthDate.set()
    else:
        await bot.send_message(message.chat.id, "Введите корректное фио")


def valid(birth_date):
    return birth_date[0].isdigit() and birth_date[1].isdigit() and birth_date[2].isdigit() and int(
        birth_date[0]) <= 31 and int(birth_date[1]) <= 12 and int(birth_date[2]) <= 2023


@dp.message_handler(state=Customer.BirthDate)
async def Customer4(message: types.Message, state: FSMContext):
    birth_date = message.text.split(".")
    if len(birth_date) == 3 and valid(birth_date):
        async with state.proxy() as data_storage:
            first_name = data_storage["first_name"]
            last_name = data_storage["last_name"]
            surname = data_storage["surname"]
            inn = data_storage["inn"]
            BotDB.add_Customer(int(inn), str(first_name), str(last_name), str(surname), str(message.text),
                               int(message.from_user.id))
            await state.finish()
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Перейти в меню",reply_markup=markup)
            markup.add(item1)
            profile = f'{last_name}\n{first_name}\n{surname}\n{inn}\n{message.text}'
            await bot.send_message(message.chat.id, "Регистрация прошла успешно!\nВаши данные:\n" + profile,)
    else:
        await bot.send_message(message.chat.id, "Введите корректную дату рождения в формате чч.мм.гг")



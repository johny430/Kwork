import sqlite3
import http.client
import json
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
from aiogram.types import *
from db import BotDB
from config import *

# инициализация базы данных
BotDB = BotDB("Kworkk.db")
conn = sqlite3.connect('Kworkk.db')
cursor = conn.cursor()

# создание объектов бота и диспетчера
bot = Bot(token=Token)
storage = MemoryStorage()
dp = Dispatcher(bot,storage=storage)

# обработчики команд
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Зарегистрироваться как заказчик")
    item2 = types.KeyboardButton("Зарегистрироваться как исполнитель")
    markup.add(item1, item2)
    await message.answer("Здравствуйте, выберите тип регистрации",reply_markup=markup)

#Создание классов для фиксации состояний
class Executor(StatesGroup):
    INN = State()
    Profile = State()

class Customer(StatesGroup):
    INN = State()
    Profile = State()
@dp.message_handler(Text(equals="Зарегистрироваться как исполнитель"))
async def executor(message: types.Message):
    await message.answer("Введите ваш ИНН для проверки")
    # if (not BotDB.executor_exists(message.from_user.id)):
    #     BotDB.add_executor(message.from_user.id)

@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    await message.answer(
        "Список доступных команд:")



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

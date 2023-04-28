import sqlite3

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor

from config import *
from db import BotDB

# инициализация базы данных
Database = BotDB("Kworkk.db")

# создание объектов бота и диспетчера
bot = Bot(token=Token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

from general import *
from GetProfile import *
from GetOrderReviews import *
from Registration import *
from Balance import *
from AddOrder import *


@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    await message.answer("Список доступных команд:")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

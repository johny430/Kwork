import sqlite3
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from db import BotDB
from config import *

# инициализация базы данных
BotDB = BotDB("Kworkk.db")
conn = sqlite3.connect('Kworkk.db')
cursor = conn.cursor()

# создание объектов бота и диспетчера
bot = Bot(token=Token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


from Executor import *
from Customer import *
from general import *
# обработчики команд
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if BotDB.executor_exists(message.from_user.id):
        await bot.send_message(message.chat.id, "Ваш профиль хуеосос!")
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Зарегистрироваться как заказчик")
        item2 = types.KeyboardButton("Зарегистрироваться как исполнитель")
        markup.add(item1, item2)
        await message.answer("Здравствуйте, выберите тип регистрации", reply_markup=markup)

@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    await message.answer(
        "Список доступных команд:")

@dp.message_handler(Text(equals="Перейти в меню"))
async def menu(message: types.Message):
    user_id = message.from_user.id
    if BotDB.executor_exists(user_id):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Баланс", reply_markup=markup)
        item2 = types.KeyboardButton("Создать анкету", reply_markup=markup)
        item3 = types.KeyboardButton("Поиск заказов", reply_markup=markup)
        markup.add(item1, item2, item3)
        await  bot.send_message(message.chat.id,"Меню",reply_markup=markup)




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

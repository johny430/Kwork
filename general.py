from main import dp
from main import bot
from main import BotDB
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram import types
import requests

@dp.message_handler(Text(equals="Перейти в меню исполнителя"))
async def menu_executor(message: types.Message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Баланс")
    item2 = types.KeyboardButton("Создать анкету")
    item3 = types.KeyboardButton("Поиск заказов")
    item4 = types.KeyboardButton("Перейти в меню заказчика")
    markup.add(item1, item2, item3,item4)
    await bot.send_message(message.chat.id,"Меню",reply_markup=markup)

@dp.message_handler(Text(equals="Перейти в меню заказчика"))
async def menu_customer(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Баланс")
    item2 = types.KeyboardButton("Создать заказ")
    item3 = types.KeyboardButton("Поиск исполнителей")
    item4 = types.KeyboardButton("Перейти в меню исполнителя")
    markup.add(item1, item2, item3, item4)
    await bot.send_message(message.chat.id, "Меню", reply_markup=markup)

@dp.message_handler(Text(equals="Баланс"))
async def balance(message: types.Message):
    user_id = message.chat.id
    balance = BotDB.get_balance(user_id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Пополнить баланс")
    back = types.KeyboardButton("Назад")
    markup.add(item1,back)
    await bot.send_message(message.chat.id, 'Ваш балланс = ' + str(balance) + " Баллов", reply_markup=markup)




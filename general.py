# from main import dp
# from main import bot
# from main import BotDB
# from aiogram.dispatcher.filters.state import State, StatesGroup
# from aiogram.dispatcher.filters import Text
# from aiogram.dispatcher import FSMContext
# from aiogram import types
# import requests
#
# @dp.message_handler(Text(equals="Перейти в меню"))
# async def menu(message: types.Message):
#     user_id = message.from_user.id
#     if BotDB.executor_exists(user_id):
#         markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#         item1 = types.KeyboardButton("Баланс", reply_markup=markup)
#         item2 = types.KeyboardButton("Создать анкету", reply_markup=markup)
#         item3 = types.KeyboardButton("Поиск заказов", reply_markup=markup)
#         markup.add(item1, item2, item3)
#         await  bot.send_message(message.chat.id,"Меню",reply_markup=markup)
#
#
# 
#

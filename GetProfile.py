from aiogram import types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters import state
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery
from Markups import back_cancel_markup, executor_menu_markup
from InlineMarkups import Choose_Profile_Markup
from main import Database
from main import bot
from main import dp


class GetProfileForm(StatesGroup):
    ProfileSelect = State()


@dp.message_handler(Text(equals="Поиск исполнителей"))
async def Search_profile(message: types.Message, state: FSMContext):
    results = Database.get_profile()
    async with state.proxy() as data_storage:
        data_storage["index"] = 0
        data_storage["data"] = results
        data_storage["message_id"] = message.message_id
    message_text = 'Список доступных исполнителей:\n'
    id = str(results[0][0])
    price = str(results[0][2])
    message_text += f'{id}. Специальность: {results[0][1]}\n Цена в час: {price}\n Описание: {results[0][3]}\n'
    await bot.send_message(message.chat.id, message_text, reply_markup=Choose_Profile_Markup)
    await GetProfileForm.ProfileSelect.set()

@dp.callback_query_handler(Text(equals='previous_profile'),state=GetProfileForm.ProfileSelect)
async def previous_result(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    async with state.proxy() as data_storage:
        index = data_storage["index"]
        if index < 1:
            return
        index -= 1
        data_storage["index"] = index
        data = data_storage["data"][index]
        message_text = f'Специальность: {data[1]}\n Цена в час: {data[2]}\n Описание: {data[3]}\n'
        await callback_query.message.edit_text(text=message_text,reply_markup= Choose_Profile_Markup)


@dp.callback_query_handler(Text(equals='next_profile'),state=GetProfileForm.ProfileSelect)
async def next_result(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    async with state.proxy() as data_storage:
        size = len(data_storage["data"])
        index = data_storage["index"]
        if index > size-2:
            return
        index += 1
        data_storage["index"] = index
        data = data_storage["data"][index]
        message_text = f'Специальность: {data[1]}\n Цена в час: {data[2]}\n Описание: {data[3]}\n'
        await callback_query.message.edit_text(text=message_text,reply_markup=Choose_Profile_Markup)






#
# @dp.message_handler(state=GetProfileForm.CoverLetter)
# async def CoverLet(message: types.Message, state: FSMContext):
#     if message.text == "Назад":
#         await bot.send_message(message.chat.id, "Меню:", reply_markup=customer_menu_markup)
#         await state.finish()
#     elif message.text == "Отмена":
#         await bot.send_message(message.chat.id, "Меню:", reply_markup=customer_menu_markup)
#         await state.finish()
#     elif message.text.isdigit():
#         id = int(message.text)
#         order = Database.get_profile_id(id)
#         if order == None:
#             await bot.send_message(message.chat.id, "Такого исполнителя не существует. Введите корректное значение!")
#         else:
#             async with state.proxy() as data_storage:
#                 data_storage["id"] = int(message.text)
#             await bot.send_message(message.chat.id, "Напишите ваше предложение с ТЗ",
#                                    reply_markup=back_cancel_markup)
#             await GetProfileForm.Mail.set()
#     else:
#         await bot.send_message(message.chat.id, "Введите корректное число!:", reply_markup=back_cancel_markup)
#
#
# @dp.message_handler(state=GetProfileForm.Mail)
# async def Mailing_cust(message: types.Message, state: FSMContext):
#     if message.text == "Назад":
#         await bot.send_message(message.chat.id, "Выберите номер заказа:", reply_markup=back_cancel_markup)
#         await GetProfileForm.CoverLetter.set()
#     elif message.text == "Отмена":
#         await bot.send_message(message.chat.id, "Меню:", reply_markup=customer_menu_markup)
#         await state.finish()
#     else:
#         async with state.proxy() as data_storage:
#             TZ = message.text
#             id = data_storage["id"]
#             message_text = f"Ваш запрос успешно отправлен исполнителю: \n{TZ}"
#             await bot.send_message(message.chat.id, message_text)
#             await bot.send_message(message.chat.id, "Меню", reply_markup=customer_menu_markup)
#             Database.add_TZ(id, TZ, message.from_user.id)
#             await state.finish()

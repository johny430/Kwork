from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from Markups import back_cancel_markup
from Markups import customer_menu_markup
from main import Database
from main import bot
from main import dp


class GetProfileForm(StatesGroup):
    GetOrder = State()
    Choose = State()
    CoverLetter = State()
    Mail = State()


@dp.message_handler(Text(equals="Поиск исполнителей"))
async def Search_profile(message: types.Message):
    results = Database.get_profile()
    message_text = 'Список доступных исполнителей:\n'
    for result in results:
        id = str(result[0])
        price = str(result[2])
        message_text += f'{id}. Специальность: {result[1]}\n Цена в час: {price}\n Описание: {result[3]}\n'
    await bot.send_message(message.chat.id, message_text, reply_markup=back_cancel_markup)
    await bot.send_message(message.chat.id, "Выберите номер исполнителя:", reply_markup=back_cancel_markup)
    await GetProfileForm.CoverLetter.set()


@dp.message_handler(state=GetProfileForm.CoverLetter)
async def CoverLet(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await bot.send_message(message.chat.id, "Меню:", reply_markup=customer_menu_markup)
        await state.finish()
    elif message.text == "Отмена":
        await bot.send_message(message.chat.id, "Меню:", reply_markup=customer_menu_markup)
        await state.finish()
    elif message.text.isdigit():
        id = int(message.text)
        order = Database.get_profile_id(id)
        if order == None:
            await bot.send_message(message.chat.id, "Такого исполнителя не существует. Введите корректное значение!")
        else:
            async with state.proxy() as data_storage:
                data_storage["id"] = int(message.text)
            await bot.send_message(message.chat.id, "Напишите ваше предложение с ТЗ",
                                   reply_markup=back_cancel_markup)
            await GetProfileForm.Mail.set()
    else:
        await bot.send_message(message.chat.id, "Введите корректное число!:", reply_markup=back_cancel_markup)


@dp.message_handler(state=GetProfileForm.Mail)
async def Mailing_cust(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await bot.send_message(message.chat.id, "Выберите номер заказа:", reply_markup=back_cancel_markup)
        await GetProfileForm.CoverLetter.set()
    elif message.text == "Отмена":
        await bot.send_message(message.chat.id, "Меню:", reply_markup=customer_menu_markup)
        await state.finish()
    else:
        async with state.proxy() as data_storage:
            TZ = message.text
            id = data_storage["id"]
            message_text = f"Ваш запрос успешно отправлен исполнителю: \n{TZ}"
            await bot.send_message(message.chat.id, message_text)
            await bot.send_message(message.chat.id, "Меню", reply_markup=customer_menu_markup)
            Database.add_TZ(id, TZ, message.from_user.id)
            await state.finish()

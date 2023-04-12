from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from Markups import back_cancel_markup
from Markups import executor_menu_markup
from main import BotDB
from main import bot
from main import dp


class GetOrderForm(StatesGroup):
    GetOrder = State()
    Choose = State()
    CoverLetter = State()
    Mail = State()


@dp.message_handler(Text(equals="Поиск заказов"))
async def Search_orders(message: types.Message):
    results = BotDB.get_orders()
    message_text = 'Список доступных Заказов:\n'
    for result in results:
        id = str(result[0])
        price = str(result[2])
        message_text += f'{id}. {result[1]}\n Цена: {price}\n Описание: {result[3]}\n'
    await bot.send_message(message.chat.id, message_text, reply_markup=back_cancel_markup)
    await bot.send_message(message.chat.id, "Выберите номер заказа:", reply_markup=back_cancel_markup)
    await GetOrderForm.CoverLetter.set()


@dp.message_handler(state=GetOrderForm.CoverLetter)
async def CL(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await bot.send_message(message.chat.id, "Меню:", reply_markup=executor_menu_markup)
        await state.finish()
    elif message.text == "Отмена":
        await bot.send_message(message.chat.id, "Меню:", reply_markup=executor_menu_markup)
        await state.finish()
    elif message.text.isdigit():
        id = int(message.text)
        order = BotDB.get_order_id(id)
        if order == None:
            await bot.send_message(message.chat.id, "Такого заказа не существует. Введите корректное значение!")
        else:
            async with state.proxy() as data_storage:
                data_storage["id"] = int(message.text)
            await bot.send_message(message.chat.id, "Напишите заказчику каким образом вы можете решить его проблему:",
                                   reply_markup=back_cancel_markup)
            await GetOrderForm.Mail.set()
    else:
        await bot.send_message(message.chat.id, "Введите корректное число!:", reply_markup=back_cancel_markup)


@dp.message_handler(state=GetOrderForm.Mail)
async def Mailing(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await bot.send_message(message.chat.id, "Выберите номер заказа:", reply_markup=back_cancel_markup)
        await GetOrderForm.CoverLetter.set()
    elif message.text == "Отмена":
        await bot.send_message(message.chat.id, "Меню:", reply_markup=executor_menu_markup)
        await state.finish()
    else:
        async with state.proxy() as data_storage:
            CoverLetter = message.text
            id = data_storage["id"]
            message_text = f"Ваше сопроводительное письмо успешно отправлено: \n{CoverLetter}"
            await bot.send_message(message.chat.id, message_text)
            await bot.send_message(message.chat.id, "Меню", reply_markup=executor_menu_markup)
            BotDB.add_CoverLetter(id, CoverLetter, message.from_user.id)
            await state.finish()

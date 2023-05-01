from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery

from InlineMarkups import Choose_Order_Markup
from Markups import executor_menu_markup, back_cancel_markup
from main import Database
from main import bot
from main import dp


class GetOrderForm(StatesGroup):
    OrderSelect = State()
    Tz = State()




@dp.message_handler(Text(equals="Поиск заказов"))
async def Search_orders(message: types.Message, state: FSMContext):
    results = Database.get_orders()
    async with state.proxy() as data_storage:
        data_storage["index"] = 0
        data_storage["data"] = results
        data_storage["message_id"] = message.message_id
    message_text = 'Список доступных Заказов:\n'
    id = str(results[0][0])
    price = str(results[0][2])
    message_text += f'{id}. {results[0][1]}\n Цена: {price}\n Описание: {results[0][3]}\n'
    await bot.send_message(message.chat.id, message_text, reply_markup=Choose_Order_Markup)
    await GetOrderForm.OrderSelect.set()

@dp.callback_query_handler(Text(equals='previous_order'),state=GetOrderForm.OrderSelect)
async def previous_result(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    async with state.proxy() as data_storage:
        index = data_storage["index"]
        if index < 1:
            return
        index -= 1
        data_storage["index"] = index
        data = data_storage["data"][index]
        message_text = f'{data[1]}\nЦена: {str(data[2])}\nОписание: {str(data[3])}\n'
        await callback_query.message.edit_text(text=message_text,reply_markup=Choose_Order_Markup)


@dp.callback_query_handler(Text(equals='next_order'),state=GetOrderForm.OrderSelect)
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
        message_text = f'{data[1]}\nЦена: {str(data[2])}\nОписание: {str(data[3])}\n'
        await callback_query.message.edit_text(text=message_text,reply_markup=Choose_Order_Markup)

@dp.callback_query_handler(Text(equals='confirm_order'), state=GetOrderForm.OrderSelect)
async def confirm_result(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    async with state.proxy() as data_storage:
        index = data_storage["index"]
        data = data_storage["data"][index]
        message_text = f'Вы выбрали:\n{data[1]}\nЦена: {str(data[2])}\nОписание: {str(data[3])}'
        await callback_query.message.edit_text(text=message_text)
        await callback_query.message.answer(text="Напишие сопроводительное письмо заказчику:",reply_markup=back_cancel_markup)
        await GetOrderForm.Tz.set()

@dp.message_handler(state=GetOrderForm.Tz)
async def send_tz(message: types.Message, state:FSMContext):
    if message.text == "Назад":
        await bot.send_message(message.chat.id, "Меню:", reply_markup=executor_menu_markup)
        await GetOrderForm.OrderSelect.set()
    elif message.text == "Отмена":
        await bot.send_message(message.chat.id, "Меню:", reply_markup=executor_menu_markup)
        await state.finish()
    else:
        CoverLatter = message.text
        async with state.proxy() as data_storage:
            index = data_storage["index"]
            Database.add_CoverLetter(index,CoverLatter,message.from_user.id)
            await bot.send_message(message.chat.id,f'Ваше сопроводительное письмо успешно отправлено:\n{CoverLatter}',reply_markup=executor_menu_markup)
            await state.finish()







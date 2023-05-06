from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery

from InlineMarkups import Choose_Profile_Markup
from Markups import customer_menu_markup, back_cancel_markup, category_markup
from main import Database
from main import bot
from main import dp


class GetProfileForm(StatesGroup):
    Category = State()
    ProfileSelect = State()
    Order = State()

@dp.message_handler(Text(equals="Поиск исполнителей"))
async def category_profile(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, "Выберите категорию заказа: ", reply_markup=category_markup)
    await GetProfileForm.Category.set()

@dp.message_handler(state= GetProfileForm.Category)
async def search_profile(message: types.Message, state: FSMContext):
    category = message.text
    try:
        results = Database.get_profile(category)
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
    except:
        await bot.send_message(message.chat.id, "В данной категории ещё нет заказов", reply_markup=category_markup)
        await GetProfileForm.Category.set()


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

@dp.callback_query_handler(Text(equals='confirm_profile'), state=GetProfileForm.ProfileSelect)
async def confirm_result(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    async with state.proxy() as data_storage:
        index = data_storage["index"]
        data = data_storage["data"][index]
        message_text = f'Специальность: {data[1]}\n Цена в час: {data[2]}\n Описание: {data[3]}\n'
        await callback_query.message.edit_text(text=message_text)
        await callback_query.message.answer(text="Напишие Ваше предложение исполнителю:",reply_markup=back_cancel_markup)
        await GetProfileForm.Order.set()

@dp.message_handler(state=GetProfileForm.Order)
async def send_tz(message: types.Message, state:FSMContext):
    if message.text == "Назад":
        await bot.send_message(message.chat.id, "Меню:", reply_markup=customer_menu_markup)
        await GetProfileForm.ProfileSelect.set()
    elif message.text == "Отмена":
        await bot.send_message(message.chat.id, "Меню:", reply_markup=customer_menu_markup)
        await state.finish()
    else:
        TZ = message.text
        async with state.proxy() as data_storage:
            index = data_storage["index"]
            Database.add_TZ(index, TZ,message.from_user.id)
            await bot.send_message(message.chat.id,f'Ваше предложение успешно отправлено:\n{TZ}',reply_markup=customer_menu_markup)
            await state.finish()

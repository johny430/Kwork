from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery

from InlineMarkups import Choose_Profile_Markup, Choose_Profile_Reviews_Markup
from Markups import executor_menu_markup
from main import bot, Database, dp


# Класс для фиксации состояний
class GetProfileReviewsForm(StatesGroup):
    ProfileReviewSelect = State()


# handler для создания заказа
@dp.message_handler(Text(equals="Посмотреть отклики на анкету"))
async def order_place(message: types.Message, state: FSMContext):
    results = Database.get_profile_for(message.from_user.id)
    async with state.proxy() as data_storage:
        data_storage["index"] = 0
        data_storage["data"] = results
        data_storage["message_id"] = message.message_id
    message_text = 'Список Ваших анкет:\n'
    id = str(results[0][0])
    price = str(results[0][4])
    message_text += f'{id}. Специальность: {results[0][2]}\n Цена в час: {price} USDT\n Описание: {results[0][3]}\n'
    await bot.send_message(message.chat.id, message_text, reply_markup=Choose_Profile_Markup)
    await GetProfileReviewsForm.ProfileReviewSelect.set()


@dp.callback_query_handler(Text(equals='previous_profile'), state=GetProfileReviewsForm.ProfileReviewSelect)
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
        await callback_query.message.edit_text(text=message_text, reply_markup=Choose_Profile_Markup)


@dp.callback_query_handler(Text(equals='next_profile'), state=GetProfileReviewsForm.ProfileReviewSelect)
async def next_result(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    async with state.proxy() as data_storage:
        size = len(data_storage["data"])
        index = data_storage["index"]
        if index > size - 2:
            return
        index += 1
        data_storage["index"] = index
        data = data_storage["data"][index]
        message_text = f'Специальность: {data[1]}\n Цена в час: {data[2]}\n Описание: {data[3]}\n'
        await callback_query.message.edit_text(text=message_text, reply_markup=Choose_Profile_Markup)


@dp.callback_query_handler(Text(equals='confirm_profile'), state=GetProfileReviewsForm.ProfileReviewSelect)
async def confirm_result(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    async with state.proxy() as data_storage:
        index = data_storage["index"]
        data = data_storage["data"][index]
        reviews = Database.get_profile_reviews(data[0])
        if len(reviews) == 0:
            await callback_query.message.answer("На данный профиль еще нет предложений!!!",
                                                reply_markup=executor_menu_markup)
            await state.finish()
        else:
            await callback_query.message.answer('Выберите понравшийся отклик на профиль')
            message_text_reviews = f'Номер: {reviews[0][0]}\nПредложенный срок (в днях): {reviews[0][2]} \nПредложенная сумма: {reviews[0][3]} USDT\nОписание: {reviews[0][4]}\n\n'
            await callback_query.message.answer(message_text_reviews, reply_markup=Choose_Profile_Reviews_Markup)

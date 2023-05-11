from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery

from InlineMarkups import Choose_Profile_Markup, Choose_Profile_Reviews_Markup, Choose_Tz_Markup
from Markups import executor_menu_markup, back_cancel_markup
from main import bot, Database, dp


# Класс для фиксации состояний
class GetProfileReviewsForm(StatesGroup):
    ProfileReviewSelect = State()
    TzSelect = State()


# handler для создания заказа
@dp.message_handler(Text(equals="Посмотреть отклики на анкету"))
async def order_place(message: types.Message, state: FSMContext):
    results = Database.get_profile_for(message.from_user.id)
    if len(results) == 0:
        await message.answer("На вашу анкету еще не откликались!\nМеню", reply_markup=executor_menu_markup)
    else:
        async with state.proxy() as data_storage:
            data_storage["index"] = 0
            data_storage["data"] = results
            data_storage["message_id"] = message.message_id
        id = str(results[0][0])
        price = str(results[0][4])
        message_text = f'{id}. Специальность: {results[0][2]}\n Цена в час: {price} USDT\n Описание: {results[0][3]}\n'
        await bot.send_message(message.chat.id, 'Список Ваших анкет:', reply_markup=back_cancel_markup)
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
        message_text = f'{data[0]}. Специальность: {data[2]}\n Цена в час: {data[4]} USDT\n Описание: {data[3]}\n'
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
        message_text = f'{data[0]}. Специальность: {data[2]}\n Цена в час: {data[4]} USDT\n Описание: {data[3]}\n'
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
            await callback_query.message.answer('Выберите понравшийся отклик на профиль',
                                                reply_markup=back_cancel_markup)
            message_text_reviews = f'Номер: {reviews[0][0]}\nПредложенный срок (в днях): {reviews[0][2]} \nПредложенная сумма: {reviews[0][3]} USDT\nОписание: {reviews[0][4]}\n\n'
            await callback_query.message.answer(message_text_reviews, reply_markup=Choose_Profile_Reviews_Markup)


@dp.callback_query_handler(Text(equals='previous_tz'), state=GetProfileReviewsForm.ProfileReviewSelect)
async def previous_result(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    print("gay")
    async with state.proxy() as data_storage:
        index = data_storage["reviews_index"]
        if index == 0:
            return
        index -= 1
        data_storage["reviews_index"] = index
        reviews = data_storage["reviews_data"][index]
        message_text_reviews = f'Номер: {reviews[0][0]}\nПредложенный срок: {reviews[0][2]} дня\nПредложенная сумма: {reviews[0][3]} USDT\nОписание: {reviews[0][4]}'
        await callback_query.message.edit_text(text=message_text_reviews, reply_markup=Choose_Tz_Markup)


@dp.callback_query_handler(Text(equals='next_tz'), state=GetProfileReviewsForm.ProfileReviewSelect)
async def next_result(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    async with state.proxy() as data_storage:
        size = len(data_storage["reviews_data"])
        index = data_storage["reviews_index"]
        if index == size - 1:
            return
        index += 1
        data_storage["reviews_index"] = index
        reviews = data_storage["reviews_data"][index]
        message_text_reviews = f'Номер: {reviews[0][0]}\nПредложенный срок (в днях): {reviews[0][2]} \nПредложенная сумма: {reviews[0][3]} USDT\nОписание: {reviews[0][4]}'
        await callback_query.message.edit_text(text=message_text_reviews, reply_markup=Choose_Tz_Markup)


@dp.callback_query_handler(Text(equals='confirm_tz'), state=GetProfileReviewsForm.ProfileReviewSelect)
async def confirm_result_profile(callback_query: CallbackQuery, state: FSMContext):
        await callback_query.answer()
        async with state.proxy() as data_storage:
            executor_id = callback_query.message.from_user.id
            customer_id = data_storage["reviews_data"][data_storage["reviews_index"]][3]
            url, chat_id = await Chat.create_group_chat_with_link(f"Заказ номер {customer_id} : {executor_id}")
            review_id = data_storage["reviews_data"][data_storage["reviews_index"]][0]
            Database.add_review_group(chat_id, review_id)
            await callback_query.message.answer(f'Для начала общения с заказчиком войдите в группу по ссылке:\n{url}',
                                                reply_markup=executor_menu_markup)
            await bot.send_message(chat_id=executor_id,
                                   text=f"Ваш отклик понравился заказчику!!!\nДля начала общения перейдите в группу по ссылке:\n{url}")


@dp.message_handler(state=GetProfileReviewsForm.ProfileReviewSelect)
async def order_place_name(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await message.answer("Меню:", reply_markup=executor_menu_markup)
        await state.finish()
    elif message.text == "Отмена":
        await message.answer("Меню:", reply_markup=executor_menu_markup)
        await state.finish()
    else:
        await message.answer("Введите корректное число!:")



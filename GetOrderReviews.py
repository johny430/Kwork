from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery

from InlineMarkups import Choose_Order_Markup
from InlineMarkups import Choose_Reviews_Markup
from Markups import back_cancel_markup
from Markups import customer_menu_markup
# from main import Chat
from main import Database
from main import bot
from main import dp


# Класс для фиксации состояний
class GetOrderReviewsForm(StatesGroup):
    ReviewSelect = State()


# handler для создания заказа
@dp.message_handler(Text(equals="Посмотреть отклики на заказ"))
async def order_place(message: types.Message, state: FSMContext):
    results = Database.get_orders_by_customer_id(message.from_user.id)
    if len(results) == 0:
        await message.answer("Ви ще не створили замовлення! Меню:", reply_markup=customer_menu_markup)
    else:
        async with state.proxy() as data_storage:
            data_storage["order_index"] = 0
            data_storage["order_data"] = results
            data_storage["order_message_id"] = message.message_id
        message_text = f'{results[0][1]}\nЦена: {str(results[0][0])}\nОписание: {str(results[0][3])}\n'
        await message.answer("Выберите заказ на который хотите посмотреть отклики:", reply_markup=back_cancel_markup)
        await message.answer(message_text, reply_markup=Choose_Order_Markup)
        await GetOrderReviewsForm.ReviewSelect.set()


@dp.callback_query_handler(Text(equals='previous_order'), state=GetOrderReviewsForm.ReviewSelect)
async def previous_result(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    async with state.proxy() as data_storage:
        index = data_storage["order_index"]
        if index == 0:
            return
        index -= 1
        data_storage["order_index"] = index
        data = data_storage["order_data"][index]
        message_text = f'{data[1]}\nЦена: {str(data[0])}\nОписание: {str(data[3])}\n'
        await callback_query.message.edit_text(text=message_text, reply_markup=Choose_Order_Markup)


@dp.callback_query_handler(Text(equals='next_order'), state=GetOrderReviewsForm.ReviewSelect)
async def next_result(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    async with state.proxy() as data_storage:
        size = len(data_storage["order_data"])
        index = data_storage["order_index"]
        if index == size - 1:
            return
        index += 1
        data_storage["order_index"] = index
        data = data_storage["order_data"][index]
        message_text = f'{data[1]}\nЦена: {str(data[0])}\nОписание: {str(data[3])}\n'
        await callback_query.message.edit_text(text=message_text, reply_markup=Choose_Order_Markup)


@dp.callback_query_handler(Text(equals='confirm_order'), state=GetOrderReviewsForm.ReviewSelect)
async def confirm_result(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    async with state.proxy() as data_storage:
        index = data_storage["order_index"]
        data = data_storage["order_data"][index]
        reviews = Database.get_orders_reviews(data[0])
        if len(reviews) == 0:
            await callback_query.message.edit_reply_markup(reply_markup=None)
            await callback_query.message.answer("На данный заказ еще нет откликов!!!",
                                                reply_markup=customer_menu_markup)
            await state.finish()
        else:
            data_storage["reviews_data"] = reviews
            data_storage["reviews_index"] = 0
            await callback_query.message.edit_reply_markup(reply_markup=None)
            await callback_query.message.answer('Выберите понравшийся отклик на зазказ')
            message_text_reviews = f'Описание: {reviews[0][2]}\n\n'
            await callback_query.message.answer(message_text_reviews, reply_markup=Choose_Reviews_Markup)


@dp.callback_query_handler(Text(equals='previous_reviews'), state=GetOrderReviewsForm.ReviewSelect)
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
        message_text_reviews = f'Описание: {reviews[2]}\n\n'
        await callback_query.message.edit_text(text=message_text_reviews, reply_markup=Choose_Reviews_Markup)


@dp.callback_query_handler(Text(equals='next_reviews'), state=GetOrderReviewsForm.ReviewSelect)
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
        message_text_reviews = f'Описание: {reviews[2]}\n\n'
        await callback_query.message.edit_text(text=message_text_reviews, reply_markup=Choose_Reviews_Markup)


@dp.callback_query_handler(Text(equals='confirm_reviews'), state=GetOrderReviewsForm.ReviewSelect)
async def confirm_result(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    async with state.proxy() as data_storage:
        customer_id = callback_query.message.from_user.id
        executor_id = data_storage["reviews_data"][data_storage["reviews_index"]][3]
        url, chat_id = await Chat.create_group_chat_with_link(f"Заказ номер {customer_id} : {executor_id}")
        print(chat_id)
        await bot.send_message(chat_id, "Привет", reply_markup=back_cancel_markup)
        await callback_query.message.answer(f'Для начала общения с заказчиком войдите в группу по ссылке:\n{url}',
                                            reply_markup=customer_menu_markup)
        await bot.send_message(chat_id=executor_id,
                               text=f"Ваш отклик понравился заказчику!!!\nДля начала общения перейдите в группу по ссылке:\n{url}")


@dp.message_handler(state=GetOrderReviewsForm.ReviewSelect)
async def order_place_name(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await message.answer("Меню:", reply_markup=customer_menu_markup)
        await state.finish()
    elif message.text == "Отмена":
        await message.answer("Меню:", reply_markup=customer_menu_markup)
        await state.finish()
    else:
        await message.answer("Введите корректное число!:", reply_markup=back_cancel_markup)

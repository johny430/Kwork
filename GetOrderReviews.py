from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery

from Markups import back_cancel_markup
from InlineMarkups import Choose_Order_Markup
from InlineMarkups import Choose_Reviews_Markup
from Markups import customer_menu_markup
from main import Database
from main import dp


# Класс для фиксации состояний
class GetOrderReviewsForm(StatesGroup):
    ReviewSelect = State()




# handler для создания заказа
@dp.message_handler(Text(equals="Посмотреть отклики на заказ"))
async def order_place(message: types.Message, state: FSMContext):
    results = Database.get_orders_for(message.from_user.id)
    async with state.proxy() as data_storage:
        data_storage["index"] = 0
        data_storage["data"] = results
        data_storage["message_id"] = message.message_id
    message_text = f'{results[0][1]}\nЦена: {str(results[0][0])}\nОписание: {str(results[0][3])}\n'
    await message.answer("Выберите заказ на который хотите посмотреть отклики:",reply_markup=back_cancel_markup)
    await message.answer(message_text, reply_markup=Choose_Order_Markup)
    await GetOrderReviewsForm.ReviewSelect.set()


@dp.callback_query_handler(Text(equals='previous_order'), state=GetOrderReviewsForm.ReviewSelect)
async def previous_result(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    async with state.proxy() as data_storage:
        index = data_storage["index"]
        if index == 0:
            return
        index -= 1
        data_storage["index"] = index
        data = data_storage["data"][index]
        message_text = f'{data[1]}\nЦена: {str(data[0])}\nОписание: {str(data[3])}\n'
        await callback_query.message.edit_text(text=message_text, reply_markup=Choose_Order_Markup)


@dp.callback_query_handler(Text(equals='next_order'), state=GetOrderReviewsForm.ReviewSelect)
async def next_result(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    async with state.proxy() as data_storage:
        size = len(data_storage["data"])
        index = data_storage["index"]
        if index == size - 1:
            return
        index += 1
        data_storage["index"] = index
        data = data_storage["data"][index]
        message_text = f'{data[1]}\nЦена: {str(data[0])}\nОписание: {str(data[3])}\n'
        await callback_query.message.edit_text(text=message_text, reply_markup=Choose_Order_Markup)

@dp.callback_query_handler(Text(equals='confirm_order'), state=GetOrderReviewsForm.ReviewSelect)
async def confirm_result(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    async with state.proxy() as data_storage:
        index = data_storage["index"]
        data = data_storage["data"][index]
        reviews = Database.get_orders_reviews(data[0])
        if len(reviews) == 0:
            await callback_query.message.answer("На данный заказ еще нет откликов!!!",
                                                reply_markup=customer_menu_markup)
            await state.finish()
        else:
            await callback_query.message.answer('Выберите понравшийся отклик на зазказ')
            message_text_reviews = f'Номер: {reviews[0][0]}\nОписание: {reviews[0][2]}\n\n'
            await callback_query.message.answer(message_text_reviews, reply_markup=Choose_Reviews_Markup)


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


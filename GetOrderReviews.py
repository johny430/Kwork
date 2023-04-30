from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from InlineMarkups import Choose_Markup
from Markups import back_cancel_markup
from Markups import customer_menu_markup
from main import Database
from main import bot
from main import dp


# Класс для фиксации состояний
class GetOrderReviewsForm(StatesGroup):
    ReviewSelect = State()
    Price = State()
    Description = State()


# handler для создания заказа
@dp.message_handler(Text(equals="Посмотреть отклики на заказ"))
async def order_place(message: types.Message, state: FSMContext):
    results = Database.get_orders()
    async with state.proxy() as data_storage:
        data_storage["index"] = 0
        data_storage["data"] = results
        data_storage["message_id"] = message.message_id
    message_text = f'{results[0][1]}\nЦена: {str(results[0][0])}\nОписание: {str(results[0][3])}\n'
    await message.answer("Выберите заказ на который хотите посмотреть отклики:")
    await message.answer(message_text, reply_markup=Choose_Markup)
    await GetOrderReviewsForm.ReviewSelect.set()

@dp.callback_query_handler(Text(equals='previous'),state=GetOrderReviewsForm.ReviewSelect)
async def previous_result(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    async with state.proxy() as data_storage:
        index = data_storage["index"]
        if index < 1:
            return
        index -= 1
        data_storage["index"] = index
        data = data_storage["data"][index]
        message_text = f'{data[1]}\nЦена: {str(data[0])}\nОписание: {str(data[3])}\n'
        await callback_query.message.edit_text(text=message_text,reply_markup=Choose_Markup)


@dp.callback_query_handler(Text(equals='next'),state=GetOrderReviewsForm.ReviewSelect)
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
        message_text = f'{data[1]}\nЦена: {str(data[0])}\nОписание: {str(data[3])}\n'
        await callback_query.message.edit_text(text=message_text,reply_markup=Choose_Markup)


@dp.callback_query_handler(Text(equals='confirm'),state=GetOrderReviewsForm.ReviewSelect)
async def confirm_result(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    async with state.proxy() as data_storage:
        index = data_storage["index"]
        data = data_storage["data"][index]
        reviews = Database.get_orders_reviews(data[0])
        if len(reviews) == 0:
            await callback_query.message.answer("На данный заказ еще нет откликов!!!\nМеню:", reply_markup=customer_menu_markup)
            await state.finish()
        else:
            await callback_query.message.answer('Выберите понравшийся отклик на зазказ')
            message_text = f'Номер: {reviews[0][0]}\nОписание: {reviews[0][2]}\n\n'
            await callback_query.message.answer(message_text, reply_markup=Choose_Markup)


# @dp.message_handler(state=GetOrderReviewsForm.ReviewSelect)
# async def order_place_name(message: types.Message, state: FSMContext):
#     if message.text == "Назад":
#         await bot.send_message(message.chat.id, "Меню:", reply_markup=customer_menu_markup)
#         await state.finish()
#     elif message.text == "Отмена":
#         await bot.send_message(message.chat.id, "Меню:", reply_markup=customer_menu_markup)
#         await state.finish()
#     elif message.text.isdigit():
#         async with state.proxy() as data_storage:
#             data_storage["id"] = int(message.text)
#         reviews = Database.get_orders_reviews(order_id=1)
#         message_text = ''
#         for review in reviews:
#             message_text += f'Номер: {review[0]}\nОписание: {review[2]}\n\n'
#         await bot.send_message(message.chat.id, "Выберите понравившийся отклик:\n" + message_text,
#                                reply_markup=back_cancel_markup)
#         await GetOrderReviewsForm.Description.set()
#     else:
#         await bot.send_message(message.chat.id, "Введите корректное число!:", reply_markup=back_cancel_markup)

#
# # handler который принимает стоимость заказа
# @dp.message_handler(state=OrderForm.Price)
# async def order_place_name(message: types.Message, state: FSMContext):
#     if message.text == "Назад":
#         await bot.send_message(message.chat.id, "Введите название заказа:", reply_markup=back_cancel_markup)
#         await OrderForm.Name.set()
#     elif message.text == "Отмена":
#         await bot.send_message(message.chat.id, "Меню:", reply_markup=customer_menu_markup)
#         await state.finish()
#     elif message.text.isdigit():
#         async with state.proxy() as data_storage:
#             data_storage["price"] = int(message.text)
#         await bot.send_message(message.chat.id, "Введите описание заказа:", reply_markup=back_cancel_markup)
#         await OrderForm.Description.set()
#     else:
#         await bot.send_message(message.chat.id, "Введите корректное число!:", reply_markup=back_cancel_markup)
#
#
# # handler который принимает описание заказа
# @dp.message_handler(state=OrderForm.Description)
# async def order_place_name(message: types.Message, state: FSMContext):
#     if message.text == "Назад":
#         await bot.send_message(message.chat.id, "Введите стоимость заказа:", reply_markup=back_cancel_markup)
#         await OrderForm.Price.set()
#     elif message.text == "Отмена":
#         await bot.send_message(message.chat.id, "Меню:", reply_markup=customer_menu_markup)
#         await state.finish()
#     else:
#         async with state.proxy() as data_storage:
#             name = data_storage["name"]
#             price = data_storage["price"]
#             description = message.text
#             message_text = f"Название: {name}\nЦена: {price} Рублей\nОписание:{description}"
#             await bot.send_message(message.chat.id, "Заказ успешно добавлен!\nДанные закаказа:" + message_text)
#             await bot.send_message(message.chat.id, "Меню", reply_markup=customer_menu_markup)
#             Database.add_order(name, price, description, message.from_user.id)
#             await state.finish()

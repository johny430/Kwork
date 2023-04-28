from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

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
async def order_place(message: types.Message):
    results = Database.get_orders()
    message_text = 'Список доступных Заказов:\n'
    for result in results:
        id = str(result[0])
        price = str(result[2])
        message_text += f'Номер: {id}. {result[1]}\n Цена: {price}\n Описание: {result[3]}\n'
    await bot.send_message(message.chat.id, message_text, reply_markup=back_cancel_markup)
    await bot.send_message(message.chat.id, "Введите номер заказа:", reply_markup=back_cancel_markup)
    await GetOrderReviewsForm.ReviewSelect.set()


@dp.message_handler(state=GetOrderReviewsForm.ReviewSelect)
async def order_place_name(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await bot.send_message(message.chat.id, "Меню:", reply_markup=customer_menu_markup)
        await state.finish()
    elif message.text == "Отмена":
        await bot.send_message(message.chat.id, "Меню:", reply_markup=customer_menu_markup)
        await state.finish()
    elif message.text.isdigit():
        async with state.proxy() as data_storage:
            data_storage["id"] = int(message.text)
        reviews = Database.get_orders_reviews(order_id=1)
        message_text = ''
        for review in reviews:
           message_text += f'Номер: {review[0]}\nОписание: {review[2]}\n\n'
        await bot.send_message(message.chat.id, "Выберите понравившийся отклик:\n" + message_text, reply_markup=back_cancel_markup)
        await GetOrderReviewsForm.Description.set()
    else:
        await bot.send_message(message.chat.id, "Введите корректное число!:", reply_markup=back_cancel_markup)

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

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ContentTypes

from Markups import back_cancel_markup, customer_menu_markup, category_markup, tz_markup
from main import bot, Database, dp


# Класс для фиксации состояний
class OrderForm(StatesGroup):
    Name = State()
    Price = State()
    Category = State()
    Deadline = State()
    Description = State()
    TechnicalTask = State()


# handler для создания заказа
@dp.message_handler(Text(equals="Создать заказ"))
async def order_place(message: types.Message):
    await bot.send_message(message.chat.id, "Введите название заказа:", reply_markup=back_cancel_markup)
    await OrderForm.Name.set()


# handler который принимает имя заказа
@dp.message_handler(state=OrderForm.Name)
async def order_place_name(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await bot.send_message(message.chat.id, "Меню:", reply_markup=customer_menu_markup)
        await state.finish()
    elif message.text == "Отмена":
        await bot.send_message(message.chat.id, "Меню:", reply_markup=customer_menu_markup)
        await state.finish()
    else:
        async with state.proxy() as data_storage:
            data_storage["name"] = message.text
        await bot.send_message(message.chat.id, "Введите стоимость заказа (B USDT):", reply_markup=back_cancel_markup)
        await OrderForm.Price.set()


@dp.message_handler(state=OrderForm.Price)
async def order_place_name(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await bot.send_message(message.chat.id, "Введите название заказа:", reply_markup=back_cancel_markup)
        await OrderForm.Name.set()
    elif message.text == "Отмена":
        await bot.send_message(message.chat.id, "Меню:", reply_markup=customer_menu_markup)
        await state.finish()
    elif message.text.isdigit():
        async with state.proxy() as data_storage:
            data_storage["price"] = int(message.text)
        await bot.send_message(message.chat.id, "Введите категорию заказа:", reply_markup=category_markup)
        await OrderForm.Category.set()
    else:
        await bot.send_message(message.chat.id, "Введите корректное число!:", reply_markup=back_cancel_markup)


# handler который принимает стоимость заказа
@dp.message_handler(state=OrderForm.Category)
async def order_place_name(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await bot.send_message(message.chat.id, "Введите стоимость заказа (B USDT):", reply_markup=back_cancel_markup)
        await OrderForm.Name.set()
    elif message.text == "Отмена":
        await bot.send_message(message.chat.id, "Меню:", reply_markup=customer_menu_markup)
        await state.finish()
    else:
        async with state.proxy() as data_storage:
            data_storage["category"] = message.text
        await bot.send_message(message.chat.id, "Каков срок исполнения заказа(в днях)?",
                               reply_markup=back_cancel_markup)
        await OrderForm.Deadline.set()


@dp.message_handler(state=OrderForm.Deadline)
async def order_place_deadline(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await bot.send_message(message.chat.id, "Введите категорию заказа:", reply_markup=category_markup)
        await OrderForm.Category.set()
    elif message.text == "Отмена":
        await bot.send_message(message.chat.id, "Меню:", reply_markup=customer_menu_markup)
        await state.finish()
    elif message.text.isdigit():
        async with state.proxy() as data_storage:
            data_storage["deadline"] = int(message.text)
        await bot.send_message(message.chat.id, "Введите описание заказа:", reply_markup=back_cancel_markup)
        await OrderForm.Description.set()
    else:
        await bot.send_message(message.chat.id, "Введите корректное число!:", reply_markup=back_cancel_markup)


# handler который принимает описание заказа
@dp.message_handler(state=OrderForm.Description)
async def order_place_name(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await bot.send_message(message.chat.id, "Каков срок исполнения заказа(в днях)?", reply_markup=category_markup)
        await OrderForm.Deadline.set()
    elif message.text == "Отмена":
        await bot.send_message(message.chat.id, "Меню:", reply_markup=customer_menu_markup)
        await state.finish()
    else:
        async with state.proxy() as data_storage:
            data_storage["description"] = message.text
        await message.answer("Сбросьте тз в виде файла:", reply_markup=tz_markup)
        await OrderForm.TechnicalTask.set()


@dp.message_handler(state=OrderForm.TechnicalTask, content_types=ContentTypes.ANY)
async def order_place_name(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await bot.send_message(message.chat.id, "Введите описание заказа:", reply_markup=back_cancel_markup)
        await OrderForm.Description.set()
    elif message.text == "Отмена":
        await bot.send_message(message.chat.id, "Меню:", reply_markup=customer_menu_markup)
        await state.finish()
    elif message.text == "Пропустить":
        async with state.proxy() as data_storage:
            name = data_storage["name"]
            price = data_storage["price"]
            category = data_storage["category"]
            deadline = data_storage["deadline"]
            description = data_storage["description"]
            message_text = f"Название: {name}\nЦена: {price} USDT\nКатегория: {category}\nСрок выполнения(в днях): {deadline}\nОписание:{description}"
            await bot.send_message(message.chat.id, "Заказ успешно добавлен!\nДанные закаказа:\n" + message_text)
            await bot.send_message(message.chat.id, "Меню", reply_markup=customer_menu_markup)
            Database.add_order(name, price, category, deadline, description, message.from_user.id)
            await state.finish()
    elif message.document:
        tz_filename = message.document.file_name
        if tz_filename.endswith(".txt") or tz_filename.endswith(".doc") or tz_filename.endswith(".docx"):
            async with state.proxy() as data_storage:
                name = data_storage["name"]
                price = data_storage["price"]
                category = data_storage["category"]
                description = data_storage["description"]
                file_id = message.document.file_id
                message_text = f"Название: {name}\nЦена: {price} USDT\nКатегория: {category}\nОписание:{description}\nФайл с тз: {tz_filename}"
                await bot.send_message(message.chat.id, "Заказ успешно добавлен!\nДанные закаказа:" + message_text)
                await bot.send_message(message.chat.id, "Меню", reply_markup=customer_menu_markup)
                Database.add_order_tz(name, price, category, description, message.from_user.id, file_id)
                await state.finish()
        else:
            await message.answer("Принимаемые форматы файлов: doc, docx, txt!!!")
    else:
        await message.answer("Отправьте тз файлом!!!")

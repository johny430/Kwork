from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import chat

from Markups import back_cancel_markup, executor_menu_markup, category_markup
from main import bot, Database, dp


# Класс для фиксации состояний
class ProfileForm(StatesGroup):
    Speciality = State()
    Price = State()
    Category = State()
    Description = State()


# handler для создания профиля
@dp.message_handler(Text(equals="Создать анкету"), chat_type=[chat.ChatType.PRIVATE])
async def profile(message: types.Message):
    await bot.send_message(message.chat.id, "Введите вашу специлизацию:", reply_markup=back_cancel_markup)
    await ProfileForm.Speciality.set()


# handler который принимает специальность исполнителя
@dp.message_handler(state=ProfileForm.Speciality)
async def Profile_Speciality(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await bot.send_message(message.chat.id, "Меню:", reply_markup=executor_menu_markup)
        await state.finish()
    elif message.text == "Отмена":
        await bot.send_message(message.chat.id, "Меню:", reply_markup=executor_menu_markup)
        await state.finish()
    else:
        async with state.proxy() as data_storage:
            data_storage["Speciality"] = message.text
        await bot.send_message(message.chat.id, "Введите вашу почасовую ставку (B USDT):",
                               reply_markup=back_cancel_markup)
        await ProfileForm.Price.set()


@dp.message_handler(state=ProfileForm.Price)
async def profile_price(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await bot.send_message(message.chat.id, "Введите вашу специализацию:", reply_markup=back_cancel_markup)
        await ProfileForm.Speciality.set()
    elif message.text == "Отмена":
        await bot.send_message(message.chat.id, "Меню:", reply_markup=executor_menu_markup)
        await state.finish()
    elif message.text.isdigit():
        async with state.proxy() as data_storage:
            data_storage["price"] = int(message.text)
        await bot.send_message(message.chat.id, "Введите категорию вашей специализации:",
                               reply_markup=category_markup)
        await ProfileForm.Category.set()
    else:
        await bot.send_message(message.chat.id, "Введите корректное число!:", reply_markup=back_cancel_markup)


# handler который принимает почасовую стоимость исполнителя
@dp.message_handler(state=ProfileForm.Category)
async def profile_price(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await bot.send_message(message.chat.id, "Введите вашу почасовую ставку (в USDT):",
                               reply_markup=back_cancel_markup)
        await ProfileForm.Price.set()
    elif message.text == "Отмена":
        await bot.send_message(message.chat.id, "Меню:", reply_markup=executor_menu_markup)
        await state.finish()
    else:
        async with state.proxy() as data_storage:
            data_storage["category"] = message.text
        await bot.send_message(message.chat.id, "Введите ваш релевантный опыт и ваши ключевые навыки:",
                               reply_markup=back_cancel_markup)
        await ProfileForm.Description.set()


# handler который принимает релевантный опыт исполнителя
@dp.message_handler(state=ProfileForm.Description)
async def order_place_name(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await bot.send_message(message.chat.id, "Введите категорию вашей специализации:", reply_markup=category_markup)
        await ProfileForm.Category.set()
    elif message.text == "Отмена":
        await bot.send_message(message.chat.id, "Меню:", reply_markup=executor_menu_markup)
        await state.finish()
    else:
        async with state.proxy() as data_storage:
            speciality = data_storage["Speciality"]
            price = data_storage["price"]
            description = message.text
            category = data_storage["category"]
            message_text = f"Ваша специальность: {speciality}\nКатегория: {category}\nВаша почасовая ставка: {price} USDT\nВаш релевантный опыт: {description}"
            await bot.send_message(message.chat.id, "Ваш профиль успешно создан!\nСодержание:\n" + message_text)
            await bot.send_message(message.chat.id, "Меню", reply_markup=executor_menu_markup)
            Database.add_profile(message.from_user.id, speciality, category, price, description)
            await state.finish()

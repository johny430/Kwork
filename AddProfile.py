from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from Markups import back_cancel_markup
from Markups import executor_menu_markup
from main import Database
from main import bot
from main import dp


# Класс для фиксации состояний
class ProfileForm(StatesGroup):
    Speciality = State()
    Price = State()
    Description = State()


# handler для создания профиля
@dp.message_handler(Text(equals="Создать анкету"))
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
        await bot.send_message(message.chat.id, "Введите вашу почасовую ставку:", reply_markup=back_cancel_markup)
        await ProfileForm.Price.set()


# handler который принимает почасовую стоимость исполнителя
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
        await bot.send_message(message.chat.id, "Введите ваш релевантный опыт и ваши ключевые навыки:",
                               reply_markup=back_cancel_markup)
        await ProfileForm.Description.set()
    else:
        await bot.send_message(message.chat.id, "Введите корректное число!:", reply_markup=back_cancel_markup)


# handler который принимает релевантный опыт исполнителя
@dp.message_handler(state=ProfileForm.Description)
async def order_place_name(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await bot.send_message(message.chat.id, "Введите вашу почасовую ставку:", reply_markup=back_cancel_markup)
        await ProfileForm.Price.set()
    elif message.text == "Отмена":
        await bot.send_message(message.chat.id, "Меню:", reply_markup=executor_menu_markup)
        await state.finish()
    else:
        async with state.proxy() as data_storage:
            speciality = data_storage["Speciality"]
            price = data_storage["price"]
            description = message.text
            message_text = f"Ваша специальность: {speciality}\nВаша почасовая ставка: {price} Рублей\nВаш релевантный опыт: {description}"
            await bot.send_message(message.chat.id, "Ваш профиль успешно создан!\nСодержание:\n" + message_text)
            await bot.send_message(message.chat.id, "Меню", reply_markup=executor_menu_markup)
            Database.add_profile(message.from_user.id, speciality, price, description)
            await state.finish()

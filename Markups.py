from aiogram import types

customer_menu_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
balance = types.KeyboardButton("Баланс")
create_order = types.KeyboardButton("Создать заказ")
find_talent = types.KeyboardButton("Поиск исполнителей")
executor_menu = types.KeyboardButton("Перейти в меню исполнителя")
customer_menu_markup.add(balance, create_order, find_talent, executor_menu)

executor_menu_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
create_questionnaire = types.KeyboardButton("Создать анкету")
find_job = types.KeyboardButton("Поиск заказов")
customer_menu = types.KeyboardButton("Перейти в меню заказчика")
executor_menu_markup.add(balance, create_questionnaire, find_job, customer_menu)

registration_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
customer_register = types.KeyboardButton("Зарегистрироваться как заказчик")
executor_register = types.KeyboardButton("Зарегистрироваться как исполнитель")
registration_markup.add(customer_register, executor_register)

balance_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
add_balance = types.KeyboardButton("Пополнить баланс")
back = types.KeyboardButton("Назад")
balance_markup.add(add_balance, back)
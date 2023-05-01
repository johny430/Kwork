from aiogram import types
from aiogram.utils.callback_data import CallbackData

callback_numbers = CallbackData("fabnum", "action")


customer_menu_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
balance = types.KeyboardButton("Баланс")
create_order = types.KeyboardButton("Создать заказ")
find_talent = types.KeyboardButton("Поиск исполнителей")
executor_menu = types.KeyboardButton("Перейти в меню исполнителя")
watch_order_review = types.KeyboardButton("Посмотреть отклики на заказ")
customer_menu_markup.row(balance, create_order, find_talent)
customer_menu_markup.row(watch_order_review)
customer_menu_markup.row(executor_menu)

executor_menu_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
create_questionnaire = types.KeyboardButton("Создать анкету")
find_job = types.KeyboardButton("Поиск заказов")
customer_menu = types.KeyboardButton("Перейти в меню заказчика")
watch_tz = types.KeyboardButton("Посмотреть отклики на анкеты")
executor_menu_markup.row(balance, create_questionnaire, find_job)
executor_menu_markup.row(watch_tz)
executor_menu_markup.row(customer_menu)

balance_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
add_balance = types.KeyboardButton("Пополнить баланс")
withdraw = types.KeyboardButton("Вывод средств")
back = types.KeyboardButton("Назад")
balance_markup.row(add_balance, withdraw)
balance_markup.row(back)

back_cancel_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
cancel = types.KeyboardButton("Отмена")
back_cancel_markup.add(back, cancel)

tz_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
skip = types.KeyboardButton("Пропустить")
tz_markup.add(back,skip,cancel)


amount_balance = types.ReplyKeyboardMarkup(resize_keyboard=True)
item5 = types.KeyboardButton("5")
item10 = types.KeyboardButton("10")
item25 = types.KeyboardButton("25")
item50 = types.KeyboardButton("50")
item100 = types.KeyboardButton("100")
amount_balance.add(item5, item10, item25, item50, item100, cancel)

confirm_payment_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
confirm_payment = types.KeyboardButton("Проверить оплату")
confirm_payment_markup.add(cancel, confirm_payment)

category_markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
design = types.KeyboardButton("Дизайн")
it = types.KeyboardButton("Разработка и IT")
text = types.KeyboardButton("Работа с текстом и перевод")
seo = types.KeyboardButton("SEO и трафик")
marketing = types.KeyboardButton("Соцсети и реклама")
audio = types.KeyboardButton("Аудио, видео, съёмка")
business = types.KeyboardButton("Бизнесс и быт")
category_markup.add(design, it, text, seo, marketing, audio, business, back, cancel)
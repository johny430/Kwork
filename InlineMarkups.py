from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

Choose_Markup = InlineKeyboardMarkup(row_width=3)
previous = InlineKeyboardButton('<', callback_data='previous')
confirm = InlineKeyboardButton('Выбрать', callback_data='confirm')
next = InlineKeyboardButton('>', callback_data='next')
Choose_Markup.add(previous,confirm, next)
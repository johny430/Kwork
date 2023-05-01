from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

Choose_Order_Markup = InlineKeyboardMarkup(row_width=3)
previous_order = InlineKeyboardButton('<', callback_data='previous_order')
confirm_order = InlineKeyboardButton('Выбрать', callback_data='confirm_order')
next_order = InlineKeyboardButton('>', callback_data='next_order')
Choose_Order_Markup.add(previous_order, confirm_order, next_order)

Choose_Review_Markup = InlineKeyboardMarkup(row_width=3)
previous_review = InlineKeyboardButton('<', callback_data='previous_review')
confirm_review = InlineKeyboardButton('Выбрать', callback_data='confirm_review')
next_review = InlineKeyboardButton('>', callback_data='next_review')
Choose_Review_Markup.add(previous_review, confirm_review, next_review)

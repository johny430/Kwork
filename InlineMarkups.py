from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

Choose_Markup = InlineKeyboardMarkup(row_width=3)
previous = InlineKeyboardButton('<', callback_data='previous')
confirm = InlineKeyboardButton('Выбрать', callback_data='confirm')
next = InlineKeyboardButton('>', callback_data='next')
Choose_Markup.add(previous,confirm, next)

switch_orders = InlineKeyboardMarkup()
back_inline = InlineKeyboardButton(text="<", callback_data="back")
approve = InlineKeyboardButton(text="Подтвердить", callback_data="approve")
forward_inline = InlineKeyboardButton(text=">", callback_data="forvard")
switch_orders.add(back_inline,approve,forward_inline)

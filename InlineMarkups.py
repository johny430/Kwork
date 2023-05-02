from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

Choose_Order_Markup = InlineKeyboardMarkup(row_width=3)
previous_order = InlineKeyboardButton('<', callback_data='previous_order')
confirm_order = InlineKeyboardButton('Выбрать', callback_data='confirm_order')
next_order= InlineKeyboardButton('>', callback_data='next_order')
Choose_Order_Markup.add(previous_order,confirm_order, next_order)

Choose_Profile_Markup = InlineKeyboardMarkup()
back_profile = InlineKeyboardButton(text="<", callback_data="previous_profile")
approve_profile = InlineKeyboardButton(text="Подтвердить", callback_data="confirm_profile")
forvard_profile = InlineKeyboardButton(text=">", callback_data="next_profile")
Choose_Profile_Markup.add(back_profile,approve_profile,forvard_profile)

Choose_Reviews_Markup = InlineKeyboardMarkup(row_width=3)
previous_reviews = InlineKeyboardButton('<', callback_data='previous_reviews')
confirm_reviews = InlineKeyboardButton('Выбрать', callback_data='confirm_reviews')
next_rewiews = InlineKeyboardButton('>', callback_data='next_rewiews')
Choose_Reviews_Markup.add(previous_reviews,confirm_reviews, next_rewiews)

Choose_Profile_Reviews_Markup = InlineKeyboardMarkup()
back_profile_reviews = InlineKeyboardButton(text="<", callback_data="back_profile_reviews")
approve_profile_reviews = InlineKeyboardButton(text="Подтвердить", callback_data="approve_profile_reviews")
forvard_profile_reviews = InlineKeyboardButton(text=">", callback_data="forvard_profile_reviews")
Choose_Profile_Reviews_Markup.add(back_profile_reviews,approve_profile_reviews,forvard_profile_reviews)
from aiogram import types

from main import Database
from main import bot
from main import dp


@dp.message_handler(chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP])
async def group_handler(message: types.Message):
    Database.add_message(message.chat.id,message.text,message.from_user.id,message.date.strftime('%H:%M:%S'))

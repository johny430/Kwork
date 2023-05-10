from aiogram import types

from main import Database
from main import dp


@dp.message_handler(commands=['confirm'], chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP])
async def group_command_handler(message: types.Message):
    executor_id = Database.get_executor_id_by_group_id(message.chat.id)
    if message.from_user.id == executor_id:
        await message.answer("Исполнитель подтвердил заказ!")
        Database.agree_executor(message.chat.id)
        if Database.conformation_count(message.chat.id) == 2:
            await message.answer("Заказ подтвержден!!!")
    else:
        await message.answer("Заказчик подтвердил заказ!")
        Database.agree_customer(group_id=message.chat.id)
        if Database.conformation_count(message.chat.id) == 2:
            await message.answer("Заказ подтвержден!!!")


@dp.message_handler(chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP])
async def group_handler(message: types.Message):
    Database.add_message(message.chat.id, message.text, message.from_user.id, message.date.strftime('%H:%M:%S'))

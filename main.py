import asyncio

import telethon
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from telethon import events, Button

from SupportClientChat import SupportClientChat
from config import *
from db import BotDB

# инициализация базы данных
Database = BotDB("Kworkk.db")
# создание объектов бота и диспетчера
bot = Bot(token=Token)
dp = Dispatcher(bot, storage=MemoryStorage())


# Chat = SupportClientChat(api_id, api_hash)


from general import *
from GetProfile import *
from GetProfileReviews import *
from GetOrder import *
from GetOrderReviews import *
from Registration import *
from Balance import *
from AddProfile import *
from AddOrder import *
from Group import *

@dp.message_handler(commands=['help'])
async def help_handler(message: types.Message):
    print(message.chat.id)
    await message.answer("Список доступных команд:")


async def main():
    # await Chat.client_start()
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

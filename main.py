import asyncio

import telethon
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import ChatTypeFilter
from telethon import events, Button

from SupportClientChat import SupportClientChat
from config import *
from db import BotDB

# инициализация базы данных
Database = BotDB("Kworkk.db")
# создание объектов бота и диспетчера
bot = Bot(token=Token)
dp = Dispatcher(bot, storage=MemoryStorage())


Chat = SupportClientChat(api_id, api_hash,"ssss")


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
from GetOrderReviews import *


async def main():
    await Chat.client_start()
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

import asyncio

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from telethon import events

from SupportClientChat import SupportClientChat
from config import *
from db import BotDB

Chat = SupportClientChat(api_id, api_hash)
# инициализация базы данных
Database = BotDB("Kworkk.db")
# создание объектов бота и диспетчера
bot = Bot(token=Token)
dp = Dispatcher(bot, storage=MemoryStorage())

from general import *
from GetProfile import *
from GetOrder import *
from GetOrderReviews import *
from Registration import *
from Balance import *
from AddOrder import *

@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    await message.answer("Список доступных команд:")


@Chat.client.on(events.NewMessage)
async def my_event_handler(event):
    print('{}'.format(event))


async def main():
    await Chat.client_start()
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

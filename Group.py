from aiogram import types
from aiogram.dispatcher.filters import ChatTypeFilter

import config
from main import Database
from main import dp
from main import bot


async def confirm_order(customer_id, executor_id, group_id):
    if Database.conformation_count(group_id) == 2:
        await bot.send_message(group_id,"Заказ подтвержден!!!")
        order = Database.get_order_by_group_id(group_id)
        customer_balance = Database.get_balance(customer_id)
        review = Database.get_review_by_group(group_id)
        price = review[3] * (1 + config.commision)
        if price > customer_balance:
            await bot.send_message(group_id,"У заказчика недостаточно средств!\nПополните баланс через бота и подтвердите заказ снова!\nТребуемая сумма {price} usdt!")
            Database.zero_conformation(group_id)
        else:
            new_balance = customer_balance - price
            Database.update_balance(customer_id,new_balance)
            Database.confirm_order_from_group(group_id)
            await bot.send_message(group_id, f"Заказ подтвержден!\nСрок выполнения(в днях): {review[1]}\nНаграда исполнителя {review[2]} usdt")



@dp.message_handler(commands=['confirm'], chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP])
async def group_command_handler(message: types.Message):
    executor_id = Database.get_executor_id_by_group_id(message.chat.id)
    customer_id = Database.get_customer_id_by_group_id(message.chat.id)
    if message.from_user.id == executor_id:
        Database.agree_executor(message.chat.id)
        await message.answer("Исполнитель подтвердил заказ!")
        await confirm_order(customer_id,executor_id,message.chat.id)
    elif message.from_user.id == customer_id:
        Database.agree_customer(message.chat.id)
        await message.answer("Заказчик подтвердил заказ!")
        await confirm_order(customer_id,executor_id,message.chat.id)


@dp.message_handler(commands=['arbitrage'], chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP])
async def group_arbitrage_handler(message: types.Message):
    await message.answer("Заявка на арбитраж отправлена!\nВам перезвонят!")
    await bot.send_message(config.admin_chat_id, f"Заявка на арбитраж в группе {message.chat.id}\nСсылка на группу {message.chat.invite_link}")


@dp.message_handler(commands=['done'], chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP])
async def group_done_handler(message: types.Message):
    customer_id = Database.get_customer_id_by_group_id(message.chat.id)
    if message.from_user.id == customer_id:
        await message.answer("Заказ выполнен успешно!\nИсполнитель получает лаве")
        Database.done_order_from_group(message.chat.id)


@dp.message_handler(chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP])
async def group_handler(message: types.Message):
    Database.add_message(message.chat.id, message.text, message.from_user.id, message.date.strftime('%H:%M:%S'))


@dp.message_handler(ChatTypeFilter(types.ChatType.GROUP), content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def handle_join(message: types.Message):
    executor_id = Database.get_executor_id_by_group_id(message.chat.id)
    customer_id = Database.get_customer_id_by_group_id(message.chat.id)
    for user in message.new_chat_members:
        if user.id == executor_id:
            await message.answer(
                "Исполнитель вошел в чат!\nДля подтверждения заказа ответьте на данное сообщение командой /confirm !\nЗаказ подтверждается при согласии обоих сторон!")
        elif user.id == customer_id:
            await message.answer(
                "Заказчик вошел в чат!\nДля подтверждения заказа ответьте на данное сообщение командой /confirm !\nЗаказ подтверждается при согласии обоих сторон!")

from aiogram import types
from aiogram.dispatcher.filters import ChatTypeFilter

import config
from main import Database
from main import bot
from main import dp


async def confirm_order(customer_id, group_id):
    if Database.conformation_count(group_id) == 2:
        await bot.send_message(group_id, "Заказ подтвержден!!!")
        customer_balance = Database.get_balance(customer_id)
        review = Database.get_review_by_group(group_id)
        group_review_id = Database.get_review_group_id(group_id)
        price = review[3] * (1 + config.commission)
        if price > customer_balance:
            await bot.send_message(group_id,
                                   f"У заказчика недостаточно средств!\nПополните баланс через бота и подтвердите заказ снова!\nТребуемая сумма {price} usdt!")
            Database.zero_conformation(group_id)
        else:
            new_balance = customer_balance - price
            Database.update_balance(customer_id, new_balance)
            Database.confirm_order_from_group(review[3], group_review_id[0])
            await bot.send_message(group_id,
                                   f"Заказ подтвержден!\nСрок выполнения(в днях): {review[2]}\nНаграда исполнителя {review[3]} usdt")


@dp.message_handler(commands=['confirm'], chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP])
async def group_command_handler(message: types.Message):
    executor_id = Database.get_executor_id_by_group_id(message.chat.id)
    customer_id = Database.get_customer_id_by_group_id(message.chat.id)
    if message.from_user.id == executor_id:
        Database.agree_executor(message.chat.id)
        await message.answer("Исполнитель подтвердил заказ!")
        await confirm_order(customer_id, executor_id, message.chat.id)
    elif message.from_user.id == customer_id:
        Database.agree_customer(message.chat.id)
        await message.answer("Заказчик подтвердил заказ!")
        await confirm_order(customer_id, executor_id, message.chat.id)


@dp.message_handler(commands=['arbitrage'], chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP])
async def group_arbitrage_handler(message: types.Message):
    await message.answer("Заявка на арбитраж отправлена!\nАдмин в пути...")
    await bot.send_message(config.admin_chat_id,
                           f"Заявка на арбитраж в группе {message.chat.id}\nСсылка на группу {message.chat.invite_link}")


@dp.message_handler(commands=['done'], chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP])
async def group_done_handler(message: types.Message):
    if Database.conformation_count(message.chat.id) == 2:
        customer_id = Database.get_customer_id_by_group_id(message.chat.id)
        if message.from_user.id == customer_id:
            await message.answer("Заказ выполнен успешно!\nИсполнитель получил деньги")
            executor_id = Database.get_executor_id_by_group_id(group_id=message.chat.id)
            confirmed_order = Database.get_confirmed_order(group_id=message.chat.id)
            new_balance = confirmed_order[1] + Database.get_balance(executor_id)
            Database.update_balance(executor_id, new_balance)
            Database.clear_by_group(message.chat.id, confirmed_order[0],
                                    Database.get_order_by_group_id(message.chat.id)[0])
            await bot.leave_chat(message.chat.id)
    else:
        await message.answer(
            "Заказ еще не подтвержден!\n Для подтверждения заказа исполнитель и закзачик должны воспользоваться командой /confirm")


@dp.message_handler(commands=['set_price'], chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP])
async def group_done_handler(message: types.Message):
    arguments = message.get_args()
    if arguments.isdigit():
        price = int(arguments)
        res = Database.get_review_by_group(message.chat.id)[0]
        Database.update_review_price(res, price)
        await message.answer(f'Новая цена: {price} USDT')
    else:
        await message.answer("Введите команду в формате /set_price 1 , где 1 - новая цена")


@dp.message_handler(commands=['set_deadline'], chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP])
async def group_done_handler(message: types.Message):
    arguments = message.get_args()
    if arguments.isdigit():
        days = int(arguments)
        res = Database.get_review_by_group(message.chat.id)[0]
        Database.update_review_dedline(res, days)
        await message.answer(f'Новый срок исполнения(в днях): {days}')
    else:
        await message.answer("Введите команду в формате /set_price 1 , где 1 - новая цена")


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
                "Исполнитель вошел в чат!\nЗдравствуйте, уважаемый пользователь\nПервым делом установите договорные условия цены командой /set_price и условия выполнения заказа в днях командой /set_deadline\nПомните, что устанавливаемая цена - размер награды, которую получит исполнитель. У заказчика на счету должна быть эта цена + 5% для коммисии площадке\nПосле полной договорённости подтвердите услновия командой /confirm\nПри возникновении спорных ситуаций воспользуйтесь командой /arbitrage для вызова админа.")
        elif user.id == customer_id:
            await message.answer(
                "Заказчик вошел в чат!\nЗдравствуйте, уважаемый пользователь\nПервым делом установите договорные условия цены командой /set_price и условия выполнения заказа в днях командой /set_deadline\nПомните, что устанавливаемая цена - размер награды, которую получит исполнитель. У заказчика на счету должна быть эта цена + 5% для коммисии площадке\nПосле полной договорённости подтвердите услновия командой /confirm\nПри возникновении спорных ситуаций воспользуйтесь командой /arbitrage для вызова админа.\nПосле полного выполнения заказа подтвердите перевод средств исполнителю командой /done ")



import http.client
import json

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State

from config import API_TOKEN
from Markups import amount_balance, balance_markup, back_cancel_markup, customer_menu_markup
from main import Database
from main import bot
from main import dp


class BalanceForm(StatesGroup):
    Check = State()
    Amount = State()
    Confirm = State()
    Withdraw = State()
    Wallet = State()


@dp.message_handler(Text(equals="Баланс"))
async def check_balance(message: types.Message, state: FSMContext):
    async with state.proxy() as data_storage:
        money = Database.get_balance(user_id=message.from_user.id)
        data_storage["money"] = money
        await bot.send_message(message.chat.id, 'Ваш балланс = ' + str(money) + " USDT", reply_markup=balance_markup)
        await BalanceForm.Check.set()


@dp.message_handler(state=BalanceForm.Check)
async def change_balance(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await bot.send_message(message.chat.id, "Меню:", reply_markup=customer_menu_markup)
        await state.finish()
    elif message.text == "Вывод средств":
        await bot.send_message(message.chat.id,"Введите количество USDT, которое вы хотите вывести:",reply_markup=back_cancel_markup)
        await BalanceForm.Withdraw.set()
    elif message.text == "Пополнить баланс":
        await bot.send_message(message.chat.id, "Введите количество:", reply_markup=amount_balance)
        await BalanceForm.Amount.set()
    else:
        await bot.send_message(message.chat.id, "Меню:", reply_markup=customer_menu_markup)
        await state.finish()

@dp.message_handler(state=BalanceForm.Amount)
async def process_name(message: types.Message, state: FSMContext):
    if message.text == "Отмена":
        user_id = message.chat.id
        balance = Database.get_balance(user_id)
        await bot.send_message(message.chat.id, 'Ваш балланс = ' + str(balance) + ' USDT', reply_markup=balance_markup)
        await BalanceForm.Check.set()
    elif message.text.isdigit():
        conn = http.client.HTTPSConnection("api.commerce.coinbase.com")
        payload = json.dumps({
        "name": "Пополнение балланса",
                "description": "FreelanceHub",
        "pricing_type": "fixed_price",
        "local_price": {
            "amount": message.text,
            "currency": "usdt"
        }
        })
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-CC-Version': '2018-03-22',
            'X-CC-Api-Key': API_TOKEN
        }
        conn.request("POST", "/charges", payload, headers)
        res = conn.getresponse()
        data = res.read()
        data = data.decode("utf-8")
        data = json.loads(data)
        address = data["data"]["addresses"]["tether"]
        id = data["data"]["id"]
        url = data["data"]["hosted_url"]
        async with state.proxy() as data_storage:
            data_storage['amount'] = float(message.text)
            data_storage['address'] = address
            data_storage["id"] = id
        await BalanceForm.Confirm.set()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        approve = types.KeyboardButton("Подтвердить оплату")
        back = types.KeyboardButton("Отмена")
        markup.add(back,approve)
        await bot.send_message(message.chat.id, "Перечислите " + message.text + "usdt на адресс:\n" + address + "\nИли оплатите по ссылке: " + url, reply_markup=markup)
    else:
        await bot.send_message(message.chat.id, 'Введите целое число!')

@dp.message_handler(state=BalanceForm.Confirm)
async def process_name2(message: types.Message,state: FSMContext):
    async with state.proxy() as data_storage:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Отмена")
        item2 = types.KeyboardButton("Проверить оплату")
        markup.add(item1,item2)
        if message.text == "Отмена":
            await bot.send_message(message.chat.id, "Меню:", reply_markup=customer_menu_markup)
            await state.finish()
        else:
            conn = http.client.HTTPSConnection("api.commerce.coinbase.com")
            payload = ''
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'X-CC-Api-Key': API_TOKEN
            }
            conn.request("GET", "/charges/" + data_storage["id"], payload, headers)
            res = conn.getresponse()
            data = res.read()
            print(data.decode("utf-8"))
            data = json.loads(data)
            status = data["data"]["timeline"][-1]["status"]
            if status == "REFOUNDED":
                #оплачено успешно
                #amount - количество usdt на которое успешно пополнили баланс
                amount = data_storage['amount']
                await state.reset_state (with_data = False)
                await bot.send_message(message.chat.id, "Оплачено успешно!",reply_markup=customer_menu_markup)
                # пополняем баланс на amount usdt
                user_id = message.chat.id
                upd_balance = Database.get_balance(user_id) + amount
                Database.update_balance(user_id, upd_balance)
                await state.finish()
            else:
                await bot.send_message(message.chat.id, "Оплата пока не найдена. Возвожно она не прошла проверку сетью.Попробуйте позже!")

@dp.message_handler(state=BalanceForm.Withdraw)
async def withdraw_amount(message: types.Message, state:FSMContext):
    if message.text == "Назад":
        await bot.send_message(message.chat.id, "Меню:", reply_markup=customer_menu_markup)
        await state.finish()
    elif message.text == "Отмена":
        await bot.send_message(message.chat.id, "Меню:", reply_markup=customer_menu_markup)
        await state.finish()
    elif message.text.isdigit():
        async with state.proxy() as data_storege:
            if int(message.text) <= int(data_storege["money"]):
                data_storege["amount"] = message.text
                await bot.send_message(message.chat.id,"Введите ваш USDT кошелек в сети TRC20",reply_markup=back_cancel_markup)
                await BalanceForm.Wallet.set()
            else:
                await bot.send_message(message.chat.id,"Недостаточно средств")
    else:
        await bot.send_message(message.chat.id, 'Введите целое число!')

@dp.message_handler(state=BalanceForm.Wallet)
async def withdraw_amount(message: types.Message, state:FSMContext):
    if message.text == "Назад":
        await bot.send_message(message.chat.id, "Введите количество USDT, которое вы хотите вывести:", reply_markup=back_cancel_markup)
        await BalanceForm.Withdraw.set()
    elif message.text == "Отмена":
        await bot.send_message(message.chat.id, "Меню:", reply_markup=customer_menu_markup)
        await state.finish()
    elif message.text[:2] == "Tx":
        async with state.proxy() as data_storage:
            amount = data_storage["amount"]
            admin_chat_id = 6221033221
            user_id = message.from_user.id
            message_text = f"Пользователь {user_id} подал запрос на вывод.\n{amount} USDT\n {message.text} - TRC20 кошелёк. "
            await bot.send_message(message.chat.id,f"Ваш запрос на вывод принят.\nКолво USDT: {amount}\nКошелёк: {message.text}\nВывод происходит каждый вторник и четверг.",reply_markup=customer_menu_markup)
            await bot.send_message(admin_chat_id,message_text)
            balance = Database.get_balance(user_id=message.from_user.id)
            upd_balance = int(balance) - int(amount)
            Database.update_balance(user_id,str(upd_balance))
            await state.finish()
    else:
        await bot.send_message(message.chat.id,"Введите кошелёк в сети TRC20",reply_markup=back_cancel_markup)
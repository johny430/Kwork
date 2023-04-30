from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.callback_data import CallbackData

from GetOrder import Search_orders
from Markups import back_cancel_markup, customer_menu_markup,callback_numbers
from main import Database
from main import bot
from main import dp

callback_numbers = CallbackData("fabnum", "action")

@dp.callback_query_handlers(callback_numbers.filter(action=["back","forward"]))
async def switch_back(call: types.CallbackQuery, state: FSMContext):
    await call.answer()


@dp.callback_query_handlers(callback_numbers.filter(action=["approve"]))
async def switch_back(call: types.CallbackQuery):

    await call.answer()
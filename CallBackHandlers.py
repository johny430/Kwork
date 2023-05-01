from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.callback_data import CallbackData

from main import dp

callback_numbers = CallbackData("fabnum", "action")


@dp.callback_query_handlers(callback_numbers.filter(action=["back", "forward"]))
async def switch_back(call: types.CallbackQuery, state: FSMContext):
    await call.answer()


@dp.callback_query_handlers(callback_numbers.filter(action=["approve"]))
async def switch_back(call: types.CallbackQuery):
    await call.answer()

from aiogram import Router
from aiogram.filters import Command
from aiogram import types
from aiogram.fsm.context import FSMContext
from db.func_for_db import update_last_activity


router = Router()


@router.message(Command("cancel"))
async def cancel_handler(message: types.Message, state: FSMContext):
    await update_last_activity(message)
    await state.clear()
    await message.answer('✅ Cancellation successful')

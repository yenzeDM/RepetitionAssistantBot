from aiogram import Router
from aiogram.filters import Command
from aiogram import types
from aiogram.fsm.context import FSMContext
from language.russian import Russian


router = Router()


@router.message(Command("cancel"))
async def cancel_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(Russian.CANCEL)

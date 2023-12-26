from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StatesGroup, State
from aiogram import types
from datetime import date
from db.func_for_db import add_data_in_db, update_last_activity
from aiogram import Router, F
from language.russian import Russian
from keyboards.client_keyboards import kb_for_add, kb_for_command_menu


available_number_for_repetition = [str(i) for i in range(1, 31)]
router = Router()


class AddText(StatesGroup):
    phrase = State()
    days_before_repetition = State()
    translation = State()


@router.message(F.text.contains('Addition'))
async def addition_handler(message: types.Message, state: FSMContext):
    await update_last_activity(message)
    await state.set_state(AddText.phrase)
    await message.answer(Russian.TEXT_TO_REPEAT, parse_mode='Markdown')


@router.message(AddText.phrase)
async def text_to_repeat_handler(message: types.Message, state: FSMContext):
    await state.update_data(user_tg_id=message.from_user.id)
    await state.update_data(phrase=message.text.lower())
    await state.set_state(AddText.translation)
    await message.answer(Russian.HELP_TEXT, parse_mode='Markdown')


@router.message(AddText.translation)
async def help_text_handler(message: types.Message, state: FSMContext):
    await state.update_data(translation=message.text.lower())
    await state.update_data(date_of_addition=str(date.today()))
    await state.set_state(AddText.days_before_repetition)
    await message.answer(Russian.DAYS_BEFORE_REPETITION)


@router.message(AddText.days_before_repetition, F.text.in_(available_number_for_repetition))
async def day_before_repetition_handler(message: types.Message, state: FSMContext):
    await state.update_data(days_before_repetition=int(message.text.strip()))
    data = await state.get_data()

    await add_data_in_db(data)
    await message.answer(Russian.POSITIVE_RESULT, reply_markup=await kb_for_add())
    await state.clear()


@router.message(AddText.days_before_repetition)
async def day_before_repetition_incorrectly_handler(message: types.Message):
    await message.answer(Russian.NEGATIVE_RESULT)


@router.callback_query(F.data == 'menu')
async def menu_handler(callback: types.callback_query):
    await callback.message.answer(Russian.MENU, reply_markup=await kb_for_command_menu())
    await callback.answer()
    await callback.message.delete()

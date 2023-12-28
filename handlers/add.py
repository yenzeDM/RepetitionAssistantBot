from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StatesGroup, State
from aiogram import types
from datetime import date
from db.func_for_db import add_data
from aiogram import Router, F
from language.russian import Russian
from keyboards.client_keyboards import kb_for_add, kb_for_command_menu


available_number_for_repetition = [str(i) for i in range(1, 31)]
router = Router()


class AddText(StatesGroup):
    text_to_repeat = State()
    help_text = State()
    days_before_repetition = State()


@router.message(F.text.contains('Addition'))
async def addition_handler(message: types.Message, state: FSMContext):
    await state.set_state(AddText.text_to_repeat)
    await message.answer(Russian.ADD_TEXT_TO_REPEAT, parse_mode='Markdown')


@router.message(AddText.text_to_repeat)
async def text_to_repeat_handler(message: types.Message, state: FSMContext):
    await state.update_data(user_tg_id=message.from_user.id)
    await state.update_data(text_to_repeat=message.text.lower())
    await state.set_state(AddText.help_text)
    await message.answer(Russian.ADD_HELP_TEXT, parse_mode='Markdown')


@router.message(AddText.help_text)
async def help_text_handler(message: types.Message, state: FSMContext):
    await state.update_data(help_text=message.text.lower())
    await state.update_data(date_of_addition=str(date.today()))
    await state.set_state(AddText.days_before_repetition)
    await message.answer(Russian.ADD_DAYS_BEFORE_REPETITION)


@router.message(AddText.days_before_repetition, F.text.in_(available_number_for_repetition))
async def day_before_repetition_handler(message: types.Message, state: FSMContext):
    await state.update_data(days_before_repetition=int(message.text.strip()))
    data = await state.get_data()

    await add_data(data)
    await message.answer(Russian.ADD_POSITIVE, reply_markup=await kb_for_add())
    await state.clear()


@router.message(AddText.days_before_repetition)
async def day_before_repetition_incorrectly_handler(message: types.Message):
    await message.answer(Russian.ADD_NEGATIVE)


@router.callback_query(F.data == 'keyboard_with_commands')
async def keyboard_with_commands_handler(callback: types.callback_query):
    await callback.message.answer(Russian.KEYBOARD_WITH_COMMANDS, reply_markup=await kb_for_command_menu())
    await callback.answer()
    await callback.message.delete()

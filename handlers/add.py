from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StatesGroup, State
from aiogram import types
from datetime import date
from db.func_for_db import add_data_in_db, update_last_activity
from aiogram import Router, F


available_number_for_repetition = [str(i) for i in range(1, 31)]
router = Router()


class AddText(StatesGroup):
    phrase = State()
    user_tg_id = State()
    days_before_repetition = State()
    translation = State()
    date_of_addition = State()


@router.message(F.text.contains('Add'))
async def start_to_add(message: types.Message, state: FSMContext):
    await update_last_activity(message)
    await state.set_state(AddText.phrase)
    await message.answer('''1️⃣

To cancel command, you should enter⚠️ /cancel

🖌 Enter anything you want to practice. It can be either a word in the language you want to practice or an answer to a rule or task:''')


@router.message(AddText.phrase)
async def add_en_phrase(message: types.Message, state: FSMContext):
    await state.update_data(user_tg_id=message.from_user.id)
    await state.update_data(phrase=message.text.lower())
    await state.set_state(AddText.translation)
    await message.answer('''2️⃣

🖌 Enter the translation of the word if you have added a word, or write a question about the rule or task if you have added an answer to them in the previous step:''')


@router.message(AddText.translation)
async def add_translation(message: types.Message, state: FSMContext):
    await state.update_data(translation=message.text.lower())
    await state.update_data(date_of_addition=str(date.today()))
    await state.set_state(AddText.days_before_repetition)
    await message.answer('''3️⃣

🖌 Enter days before repetition from 1️⃣ to 3️⃣0️⃣:''')


@router.message(AddText.days_before_repetition, F.text.in_(available_number_for_repetition))
async def add_day_before_repetition(message: types.Message, state: FSMContext):
    await state.update_data(days_before_repetition=int(message.text.strip()))
    data = await state.get_data()

    await add_data_in_db(data)
    await message.answer('✅ You have successfully added new text.')
    await state.clear()


@router.message(AddText.days_before_repetition)
async def add_day_before_repetition_incorrectly(message: types.Message):
    await message.answer('❌ You have specified an incorrect number, please choose a number from 1️⃣ to 3️⃣0️⃣:')

from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StatesGroup, State
from aiogram import types
from db.func_for_db import update_last_activity, show_list_of_phrases, change_days_before_repetition
from aiogram import Router, F
from asyncio import sleep
from additional_func import handler_for_show_list


available_number_for_repetition = [str(i) for i in range(1, 31)]
router = Router()


class ChangedDaysBeforeRepetition(StatesGroup):
    phrase = State()
    change = State()


@router.message(F.text.contains('Change'))
async def command_changed(message: types.Message, state: FSMContext):
    await update_last_activity(message)
    await state.set_state(ChangedDaysBeforeRepetition.phrase)
    all_phrases = await show_list_of_phrases(message)
    if all_phrases:
        if len(all_phrases) > 100:
            while all_phrases:
                await message.answer(await handler_for_show_list(all_phrases[0:99], translation=True, days=True))
                await sleep(0.5)
                all_phrases = all_phrases[99::]
            await message.answer('🖌 Copy and enter your phrase above without the days only the text where you want to change days before repetition:')
        else:
            await message.answer(await handler_for_show_list(all_phrases, translation=True, days=True))
            await sleep(0.5)
            await message.answer('🖌 Copy and enter your phrase above without the days only the text where you want to change days before repetition:')
    else:
        await message.answer('You have nothing in your dictionary 🗑')
        await state.clear()


@router.message(ChangedDaysBeforeRepetition.phrase)
async def command_phrase(message: types.Message, state: FSMContext):
    await state.update_data(translation=message.text.lower())
    await state.set_state(ChangedDaysBeforeRepetition.change)
    await message.answer('🖌 Enter days before repetition from 1️⃣ to 3️⃣0️⃣:')


@router.message(ChangedDaysBeforeRepetition.change, F.text.in_(available_number_for_repetition))
async def add_day_before_repetition(message: types.Message, state: FSMContext):
    await state.update_data(days_before_repetition=int(message.text.strip()))
    data = await state.get_data()
    try:
        await change_days_before_repetition(data, message)
        await message.answer('✅ You have successfully changed days before repetition.')
        await state.clear()
    except:
        await message.answer('❌ You do not have this text in your dictionary try again')
        await state.clear()


@router.message(ChangedDaysBeforeRepetition.change)
async def add_day_before_repetition_incorrectly(message: types.Message):
    await message.answer('❌ You have specified an incorrect number, please choose a number from 1️⃣ to 3️⃣0️⃣:')

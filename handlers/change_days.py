from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StatesGroup, State
from aiogram import types
from db.func_for_db import show_all_added_material, change_days_before_repetition
from aiogram import Router, F
from asyncio import sleep
from additional_func import change_list_output
from language.russian import Russian


available_number_for_repetition = [str(i) for i in range(1, 31)]
router = Router()


class ChangedDaysBeforeRepetition(StatesGroup):
    text_to_repeat = State()
    change = State()


@router.message(F.text.contains('Change'))
async def change_handler(message: types.Message, state: FSMContext):
    await state.set_state(ChangedDaysBeforeRepetition.text_to_repeat)
    all_material = await show_all_added_material(message)
    if all_material:
        if len(all_material) > 100:
            while all_material:
                await message.answer(await change_list_output(all_material[0:99], help_text=True, days=True))
                await sleep(0.5)
                all_material = all_material[99::]
            await message.answer(Russian.CHANGE_HELP_TEXT, parse_mode='Markdown')
        else:
            await message.answer(await change_list_output(all_material, help_text=True, days=True))
            await sleep(0.5)
            await message.answer(Russian.CHANGE_HELP_TEXT, parse_mode='Markdown')
    else:
        await message.answer(Russian.CHANGE_EMPTY)
        await state.clear()


@router.message(ChangedDaysBeforeRepetition.text_to_repeat)
async def help_text_handler(message: types.Message, state: FSMContext):
    await state.update_data(help_text=message.text.lower())
    await state.set_state(ChangedDaysBeforeRepetition.change)
    await message.answer(Russian.CHANGE_DAYS_BEFORE_REPETITION)


@router.message(ChangedDaysBeforeRepetition.change, F.text.in_(available_number_for_repetition))
async def day_before_repetition_handler(message: types.Message, state: FSMContext):
    await state.update_data(days_before_repetition=int(message.text.strip()))
    data = await state.get_data()
    try:
        await change_days_before_repetition(data, message)
        await message.answer(Russian.CHANGE_POSITIVE)
        await state.clear()
    except:
        await message.answer(Russian.CHANGE_NEGATIVE_TEXT)
        await state.clear()


@router.message(ChangedDaysBeforeRepetition.change)
async def day_before_repetition_incorrectly_handler(message: types.Message):
    await message.answer(Russian.CHANGE_NEGATIVE_NUM)

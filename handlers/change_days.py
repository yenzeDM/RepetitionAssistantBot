from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StatesGroup, State
from aiogram import types
from db.func_for_db import show_all_added_material, change_by_days, get_days_before_repetition, get_text_to_repeat, change_several, change_one
from aiogram import Router, F
from additional_func import divide
from language.russian import Russian
from keyboards.client_keyboards import kb_for_change


available_number_for_repetition = [str(i) for i in range(1, 31)]
router = Router()


class ChangeDaysBeforeRepetition(StatesGroup):
    choose_change_type = State()
    change_by_days = State()
    change_several = State()
    change_one = State()


@router.message(F.text.contains('Change'))
async def change_days_handler(message: types.Message, state: FSMContext):
    if await show_all_added_material(message):
        await state.set_state(ChangeDaysBeforeRepetition.choose_change_type)
        await message.answer(Russian.CHANGE_DAYS_TYPE_OF_CHANGE, reply_markup=await kb_for_change())
    else:
        await message.answer(Russian.CHANGE_EMPTY)


@router.callback_query(F.data == 'change_by_days', )
async def change_by_days_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(Russian.CHANGE_BY_DAYS_OLD)
    await state.update_data(change_type=callback.data)
    await callback.answer()


@router.callback_query(F.data == 'change_several')
async def change_several_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(Russian.CHANGE_DAYS_BEFORE_REPETITION)
    await state.update_data(change_type=callback.data)
    await callback.answer()


@router.callback_query(F.data == 'change_one')
async def change_one_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(Russian.CHANGE_DAYS_BEFORE_REPETITION)
    await state.update_data(change_type=callback.data)
    await callback.answer()


@router.message(ChangeDaysBeforeRepetition.choose_change_type)
async def change_days_type_handler(message: types.Message, state: FSMContext):
    change_type = await state.get_data()
    if change_type['change_type'] == 'change_by_days':
        old_days_in_dictionary = [i[0] for i in await get_days_before_repetition(message)]
        try:
            if int(message.text.strip()) in old_days_in_dictionary:
                await state.update_data(old_days=int(message.text.strip()))
                await state.set_state(ChangeDaysBeforeRepetition.change_by_days)
                await message.answer(Russian.CHANGE_DAYS_BEFORE_REPETITION)
            else:
                await message.answer(Russian.CHANGE_BY_DAYS_NEGATIVE)
                await state.clear()
        except:
            await message.answer(Russian.CHANGE_BY_DAYS_NEGATIVE)
            await state.clear()
    if change_type['change_type'] == 'change_several':
        if message.text.strip() in available_number_for_repetition:
            await state.update_data(new_days=int(message.text.strip()))
            await state.set_state(ChangeDaysBeforeRepetition.change_several)
            await message.answer(Russian.CHANGE_SEVERAL, parse_mode='Markdown')
        else:
            await message.answer(Russian.CHANGE_SEVERAL_NEGATIVE_NUM)
            await state.clear()
    if change_type['change_type'] == 'change_one':
        if message.text.strip() in available_number_for_repetition:
            await state.update_data(new_days=int(message.text.strip()))
            await state.set_state(ChangeDaysBeforeRepetition.change_one)
            await message.answer(Russian.CHANGE_ONE, parse_mode='Markdown')
        else:
            await message.answer(Russian.CHANGE_ONE_NEGATIVE_NUM)
            await state.clear()


@router.message(ChangeDaysBeforeRepetition.change_by_days, F.text.in_(available_number_for_repetition))
async def finish_change_by_days_handler(message: types.Message, state: FSMContext):
    await state.update_data(new_days=int(message.text.strip()))
    data = await state.get_data()
    await change_by_days(data, message)
    await message.answer(Russian.CHANGE_POSITIVE)
    await state.clear()


@router.message(ChangeDaysBeforeRepetition.change_by_days)
async def finish_change_by_days_incorrectly_handler(message: types.Message):
    await message.answer(Russian.CHANGE_BY_DAYS_NEGATIVE_NUM)


@router.message(ChangeDaysBeforeRepetition.change_several)
async def finish_change_several_handler(message: types.Message, state: FSMContext):
    text_to_repeat = [i[0] for i in await get_text_to_repeat(message)]
    phrases_for_change = await divide(message.text, ',')
    data = await state.get_data()
    try:
        for text in phrases_for_change:
            if text.strip() in text_to_repeat:
                await change_several(data['new_days'], text.strip(), message)
            else:
                await message.answer(f'<b>{text.strip()}</b>\n\n{Russian.CHANGE_SEVERAL_NEGATIVE_TEXT}', parse_mode='HTML')
                raise ValueError('Invalid text to delete')
        await message.answer(Russian.CHANGE_POSITIVE)
        await state.clear()
    except:
        await state.clear()


@router.message(ChangeDaysBeforeRepetition.change_one)
async def finish_change_one_handler(message: types.Message, state: FSMContext):
    await state.update_data(text_to_repeat=message.text.strip())
    data = await state.get_data()
    try:
        await change_one(data, message)
        await message.answer(Russian.CHANGE_POSITIVE)
        await state.clear()
    except:
        await message.answer(Russian.CHANGE_ONE_NEGATIVE_TEXT)
        await state.clear()
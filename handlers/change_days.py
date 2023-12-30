from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StatesGroup, State
from aiogram import types
from db.func_for_db import show_all_added_material, change_days_before_repetition, change_by_days, get_days_before_repetition
from aiogram import Router, F
from asyncio import sleep
from additional_func import change_list_output, divide
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
    await callback.message.answer(Russian.CHANGE_SEVERAL)
    await state.update_data(change_type=callback.data)
    await callback.answer()


@router.callback_query(F.data == 'change_one')
async def change_one_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(Russian.CHANGE_ONE)
    await state.update_data(change_type=callback.data)
    await callback.answer()


@router.message(ChangeDaysBeforeRepetition.choose_change_type)
async def change_days_type_handler(message: types.Message, state: FSMContext):
    change_type = await state.get_data()
    if change_type['change_type'] == 'change_by_days':
        old_days_in_dictionary = [i[0] for i in await get_days_before_repetition(message)]
        if int(message.text.strip()) in old_days_in_dictionary:
            await state.update_data(old_days=int(message.text.strip()))
            await state.set_state(ChangeDaysBeforeRepetition.change_by_days)
            await message.answer(Russian.CHANGE_BY_DAYS_NEW)
        else:
            await message.answer(Russian.CHANGE_BY_DAYS_NEGATIVE)
            await state.clear()
    if change_type['change_type'] == 'change_several':
        phrases_for_change = await divide(message.text, ',')


@router.message(ChangeDaysBeforeRepetition.change_by_days, F.text.in_(available_number_for_repetition))
async def finish_change_by_days_handler(message: types.Message, state: FSMContext):
    await state.update_data(new_days=int(message.text.strip()))
    data = await state.get_data()
    await change_by_days(data, message)
    await message.answer(Russian.CHANGE_POSITIVE)
    await state.clear()


@router.message(ChangeDaysBeforeRepetition.change_by_days)
async def finish_change_by_days_incorrectly_handler(message: types.Message):
    await message.answer(Russian.CHANGE_NEGATIVE_NUM)

# @router.message(F.text.contains('Change'))
# async def change_handler(message: types.Message, state: FSMContext):
#     await state.set_state(ChangedDaysBeforeRepetition.text_to_repeat)
#     all_material = await show_all_added_material(message)
#     if all_material:
#         if len(all_material) > 100:
#             while all_material:
#                 await message.answer(await change_list_output(all_material[0:99], help_text=True, days=True))
#                 await sleep(0.5)
#                 all_material = all_material[99::]
#             await message.answer(Russian.CHANGE_HELP_TEXT, parse_mode='Markdown')
#         else:
#             await message.answer(await change_list_output(all_material, help_text=True, days=True))
#             await sleep(0.5)
#             await message.answer(Russian.CHANGE_HELP_TEXT, parse_mode='Markdown')
#     else:
#         await message.answer(Russian.CHANGE_EMPTY)
#         await state.clear()


# @router.message(ChangedDaysBeforeRepetition.text_to_repeat)
# async def help_text_handler(message: types.Message, state: FSMContext):
#     await state.update_data(help_text=message.text.lower())
#     await state.set_state(ChangedDaysBeforeRepetition.change)
#     await message.answer(Russian.CHANGE_DAYS_BEFORE_REPETITION)


# @router.message(ChangedDaysBeforeRepetition.change, F.text.in_(available_number_for_repetition))
# async def day_before_repetition_handler(message: types.Message, state: FSMContext):
#     await state.update_data(days_before_repetition=int(message.text.strip()))
#     data = await state.get_data()
#     try:
#         await change_days_before_repetition(data, message)
#         await message.answer(Russian.CHANGE_POSITIVE)
#         await state.clear()
#     except:
#         await message.answer(Russian.CHANGE_NEGATIVE_TEXT)
#         await state.clear()


# @router.message(ChangedDaysBeforeRepetition.change)
# async def day_before_repetition_incorrectly_handler(message: types.Message):
#     await message.answer(Russian.CHANGE_NEGATIVE_NUM)

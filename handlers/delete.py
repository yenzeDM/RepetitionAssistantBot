from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StatesGroup, State
from aiogram import types
from db.func_for_db import update_last_activity, show_list_of_phrases, delete_one, delete_all_data_from_phrases, delete_several
from keyboards.client_keyboards import kb_for_delete
from create_bot import bot
from additional_func import divide
from language.russian import Russian


router = Router()


class DeleteText(StatesGroup):
    choose_deletion_type = State()
    finish_delete_several = State()


@router.message(F.text.contains('Deletion'))
async def delete_text_handler(message: types.Message, state: FSMContext):
    await update_last_activity(message)
    if await show_list_of_phrases(message):
        await state.set_state(DeleteText.choose_deletion_type)
        await message.answer(Russian.DELETE_TEXT_TYPE_OF_DELETION, reply_markup=await kb_for_delete())
    else:
        await message.answer(Russian.DELETE_TEXT_EMPTY)


@router.callback_query(F.data == 'delete_all')
async def delete_all_handler(callback: types.CallbackQuery, state: FSMContext):
    if show_list_of_phrases(callback):
        await callback.message.delete()
        await delete_all_data_from_phrases(callback.from_user.id)
        await callback.message.answer(Russian.DELETE_ALL_POSITIVE)
        await callback.answer()
        await state.clear()


@router.callback_query(F.data == 'delete_several')
async def delete_several_handler(callback: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback.from_user.id, Russian.DELETE_SEVERAL_TEXT_TO_REPEAT, parse_mode='Markdown')
    await callback.message.delete()
    await state.update_data(deletion_type=callback.data)
    await callback.answer()


@router.callback_query(F.data == 'delete_one')
async def delete_one_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(Russian.DELETE_ONE_TEXT_TO_REPEAT, parse_mode='Markdown')
    await state.update_data(deletion_type=callback.data)
    await callback.answer()


@router.message(DeleteText.choose_deletion_type)
async def finish_delete_text_handler(message: types.Message, state: FSMContext):
    deletion_type = await state.get_data()
    if deletion_type['deletion_type'] == 'delete_several':
        try:
            phrases_for_deletion = await divide(message.text, ',')
            await delete_several(phrases_for_deletion, message)
            await message.answer(Russian.DELETE_SEVERAL_POSITIVE)
            await state.clear()
        except:
            await message.answer(Russian.DELETE_SEVERAL_NEGATIVE)
            await state.clear()
    elif deletion_type['deletion_type'] == 'delete_one':
        try:
            await delete_one(message)
            await message.answer(Russian.DELETE_ONE_POSITIVE)
            await state.clear()
        except:
            await message.answer(Russian.DELETE_ONE_NEGATIVE)
            await state.clear()

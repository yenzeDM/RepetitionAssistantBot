from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StatesGroup, State
from aiogram import types
from db.func_for_db import update_last_activity, show_list_of_phrases, delete_specific_phrase, delete_all_data_from_phrases, delete_several_phrases
from keyboards.client_keyboards import kb_for_delete
from create_bot import bot
from additional_func import divide


router = Router()


class DeleteText(StatesGroup):
    choose_type_of_deletion = State()
    finish_delete_several = State()


@router.message(F.text.contains('Deletion'))
async def delete_text(message: types.Message, state: FSMContext):
    await update_last_activity(message)
    if await show_list_of_phrases(message):
        await state.set_state(DeleteText.choose_type_of_deletion)
        await message.answer('Choose type of deletion', reply_markup=await kb_for_delete())
    else:
        await message.answer('Your dictionary is empty 🗑')


@router.callback_query(F.data == 'delete_all')
async def delete_all(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await delete_all_data_from_phrases(callback.from_user.id)
    await callback.message.answer('✅ You deleted all phrases successful')
    await callback.answer()
    await state.clear()


@router.callback_query(F.data == 'delete_several')
async def delete_several(callback: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback.from_user.id, 'To cancel command, you should enter⚠️ /cancel\n\n✍Enter several phrases to delete separated by commas _(Enter the text that you added in the first step of the "Add text" command.)_:', parse_mode='Markdown')
    await callback.message.delete()
    await state.update_data(type_of_deletion=callback.data)
    await callback.answer()


@router.callback_query(F.data == 'delete_one')
async def delete_one(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer('To cancel command, you should enter⚠️ /cancel\n\n✍️Enter the text that you want to delete _(Enter the text that you added in the first step of the "Add text" command.)_:', parse_mode='Markdown')
    await state.update_data(type_of_deletion=callback.data)
    await callback.answer()


@router.message(DeleteText.choose_type_of_deletion)
async def delete_text(message: types.Message, state: FSMContext):
    type_of_deletion = await state.get_data()
    if type_of_deletion['type_of_deletion'] == 'delete_several':
        try:
            phrases_for_deletion = await divide(message.text, ',')
            await delete_several_phrases(phrases_for_deletion, message)
            await message.answer('✅ Deletion successful')
            await state.clear()
        except:
            await message.answer(
                '❌ An error occurred, please check if all the phrases are separated by commas and if they are in your dictionary.')
            await state.clear()
    elif type_of_deletion['type_of_deletion'] == 'delete_one':
        try:
            await delete_specific_phrase(message)
            await message.answer('✅ Deletion successful')
            await state.clear()
        except:
            await message.answer('❌ You do not have it in your dictionary')
            await state.clear()

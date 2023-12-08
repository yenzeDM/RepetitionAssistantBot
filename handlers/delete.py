from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StatesGroup, State
from aiogram import types
from db.func_for_db import update_last_activity, show_list_of_phrases, delete_specific_phrase


router = Router()


class DeleteText(StatesGroup):
    delete_en_phrase = State()


@router.message(F.text.contains('Delete'))
async def delete_text(message: types.Message, state: FSMContext):
    await update_last_activity(message)
    if await show_list_of_phrases(message):
        await state.set_state(DeleteText.delete_en_phrase)
        await message.answer('To cancel command, you should enter⚠️ /cancel\n\n✍️Enter the text that you want to delete _(Enter the text that you added in the first step of the "Add text" command.)_:', parse_mode='Markdown')
    else:
        await message.answer('Your dictionary is empty 🗑')


@router.message(DeleteText.delete_en_phrase)
async def finish_delete_text(message: types.Message, state: FSMContext):
    try:
        await delete_specific_phrase(message)
        await message.answer('✅ Deletion successful')
        await state.clear()
    except:
        await message.answer('❌ You do not have it in your dictionary')
        await state.clear()

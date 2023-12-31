from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StatesGroup, State
from aiogram import types
from db.func_for_db import show_all_added_material, delete_one, delete_all, delete_several, get_text_to_repeat
from keyboards.client_keyboards import kb_for_delete
from additional_func import divide
from language.russian import Russian


router = Router()


class DeleteText(StatesGroup):
    choose_deletion_type = State()


@router.message(F.text.contains('Deletion'))
async def delete_text_handler(message: types.Message, state: FSMContext):
    if await show_all_added_material(message):
        await state.set_state(DeleteText.choose_deletion_type)
        await message.answer(Russian.DELETE_TEXT_TYPE_OF_DELETION, reply_markup=await kb_for_delete())
    else:
        await message.answer(Russian.DELETE_TEXT_EMPTY)


@router.callback_query(F.data == 'delete_all')
async def delete_all_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await delete_all(callback.from_user.id)
    await callback.message.answer(Russian.DELETE_ALL_POSITIVE)
    await callback.answer()
    await state.clear()


@router.callback_query(F.data == 'delete_several')
async def delete_several_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(Russian.DELETE_SEVERAL_TEXT_TO_REPEAT, parse_mode='Markdown')
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
    text_to_repeat = [i[0] for i in await get_text_to_repeat(message)]
    if deletion_type['deletion_type'] == 'delete_several':
        phrases_for_deletion = await divide(message.text, ',')
        try:
            for text in phrases_for_deletion:
                if text.strip() in text_to_repeat:
                    await delete_several(text.strip(), message)
                else:
                    await message.answer(f'<b>{text.strip()}</b>\n\n{Russian.DELETE_SEVERAL_NEGATIVE}', parse_mode='HTML')
                    raise ValueError('Invalid text to delete')
            await message.answer(Russian.DELETE_SEVERAL_POSITIVE)
            await state.clear()
        except:
            await state.clear()
    elif deletion_type['deletion_type'] == 'delete_one':
        if message.text.strip() in text_to_repeat:
            await delete_one(message)
            await message.answer(Russian.DELETE_ONE_POSITIVE)
            await state.clear()
        else:
            await message.answer(Russian.DELETE_ONE_NEGATIVE)
            await state.clear()

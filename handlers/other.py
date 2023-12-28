from aiogram import Router, F
from aiogram.filters import Command
from aiogram import types
from db.func_for_db import add_user_id_in_db, update_last_activity, show_list_of_phrases
from keyboards.client_keyboards import kb_for_command_menu
from additional_func import change_list_output
from asyncio import sleep
from language.russian import Russian


router = Router()
# Доделать update_last_activity
date_of_last_activity = ''


@router.message(Command("start"))
async def start_handler(message: types.Message):
    try:
        add_user_id_in_db(message)
        await message.answer(Russian.START, parse_mode='HTML')
    except:
        await update_last_activity(message)
        await message.answer(Russian.START, parse_mode='HTML')


@router.message(Command("help"))
async def help_handler(message: types.Message):
    await message.answer(Russian.HELP, parse_mode='HTML')


@router.message(Command("menu"))
async def keyboard_with_commands_handler(message: types.Message):
    await update_last_activity(message)
    await message.answer(Russian.KEYBOARD_WITH_COMMANDS, reply_markup=await kb_for_command_menu())


@router.message(F.text.contains("List"))
async def show_list_handler(message: types.Message):
    await update_last_activity(message)
    try:
        all_phrases = await show_list_of_phrases(message)
        if len(all_phrases) > 100:
            while all_phrases:
                await message.answer(await change_list_output(all_phrases[0:99], text_to_repeat=True, help_text=True, days=True), parse_mode='Markdown')
                await sleep(0.5)
                all_phrases = all_phrases[99::]
        else:
            await message.answer(await change_list_output(all_phrases, text_to_repeat=True, help_text=True, days=True), parse_mode='Markdown')
    except:
        await message.answer(Russian.LIST_EMPTY)


@router.message(F.text)
async def spam_handler(message: types.Message):
    await update_last_activity(message)
    await message.delete()

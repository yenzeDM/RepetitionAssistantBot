from aiogram import Router, F
from aiogram.filters import Command
from aiogram import types
from db.func_for_db import add_user_id, show_all_added_material, update_last_activity
from keyboards.client_keyboards import kb_for_command_menu
from additional_func import change_list_output
from asyncio import sleep
from language.russian import Russian


router = Router()


@router.message(Command("start"))
async def start_handler(message: types.Message):
    try:
        add_user_id(message)
        await message.answer(Russian.START, parse_mode='HTML')
    except:
        await message.answer(Russian.START, parse_mode='HTML')


@router.message(Command("help"))
async def help_handler(message: types.Message):
    await message.answer(Russian.HELP, parse_mode='HTML')


@router.message(Command("keyboard_with_commands"))
async def keyboard_with_commands_handler(message: types.Message):
    await message.answer(Russian.KEYBOARD_WITH_COMMANDS, reply_markup=await kb_for_command_menu())


@router.message(F.text.contains("List"))
async def show_list_handler(message: types.Message):
    await update_last_activity(message)
    try:
        all_material = await show_all_added_material(message)
        if len(all_material) > 100:
            while all_material:
                await message.answer(await change_list_output(all_material[0:99], text_to_repeat=True, help_text=True, days=True), parse_mode='Markdown')
                await sleep(0.5)
                all_material = all_material[99::]
        else:
            await message.answer(await change_list_output(all_material, text_to_repeat=True, help_text=True, days=True), parse_mode='Markdown')
    except:
        await message.answer(Russian.LIST_EMPTY)


@router.message(F.text)
async def spam_handler(message: types.Message):
    await message.delete()

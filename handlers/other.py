from aiogram import Router, F
from aiogram.filters import Command
from aiogram import types
from db.func_for_db import add_user_id_in_db, update_last_activity, show_list_of_phrases, delete_all_data_from_phrases
from bot import bot
from keyboards.client_keyboards import kb_for_command_menu
from additional_func import handler_for_show_list
from asyncio import sleep


router = Router()


@router.message(Command("start"))
async def command_start(message: types.Message):
    try:
        add_user_id_in_db(message)
        await message.answer("""👋 Hello, I'm your <b>Repetition Assistant</b>.

▪️To start adding your any text, you need to enter the /menu command. 

▪️Use the /help command to see <b>all available commands</b> and <b>their detailed descriptions</b>.""", parse_mode='HTML')
    except:
        await update_last_activity(message)
        await message.answer("""👋 Hello, I'm your <b>Repetition Assistant</b>.

▪️To start adding your any text, you need to enter the /menu command. 

▪️Use the /help command to see <b>all available commands</b> and <b>their detailed descriptions</b>.""", parse_mode='HTML')


@router.message(Command("help"))
async def command_help(message: types.Message):
    await message.answer('''🔻 /start - start the bot.
🔸 /help - detailed instructions.
🔹 /menu - call the menu with the main commands.
▪️ /delete_all - delete all text from the dictionary.
▫️ /cancel - cancel the action of the command located in the menu.

<b>Description of commands from the menu:</b>

📓 <b>Learning</b> - start learning. You can also use this command by typing <b>"Learning"</b> in the chat with the bot.

🧾 <b>List of phrases</b> - shows everything you have added. You can also use this command by typing <b>"List"</b> in the chat with the bot.

📨 <b>Add phrase</b> - adding text to your dictionary with the indication of how many days should pass before repetition. You can also use this command by typing <b>"Add"</b> in the chat with the bot.

✂️ <b>Delete phrase</b> - Delete a specific phrase or word from your dictionary. You can also use this command by typing <b>"Delete"</b> in the chat with the bot.''', parse_mode='HTML')


@router.message(Command("menu"))
async def command_menu(message: types.Message):
    await update_last_activity(message)
    await message.answer('Choose any command', reply_markup=await kb_for_command_menu())


@router.message(F.text.contains("List"))
async def command_show(message: types.Message):
    await update_last_activity(message)
    try:
        all_phrases = await show_list_of_phrases(message)
        if len(all_phrases) > 100:
            while all_phrases:
                await message.answer(await handler_for_show_list(all_phrases[0:99], phrase=True, translation=True, date=True, days=True))
                await sleep(0.5)
                all_phrases = all_phrases[99::]
        else:
            await message.answer(await handler_for_show_list(all_phrases, phrase=True, translation=True, date=True, days=True))
    except:
        await message.answer('You have nothing in your dictionary 🗑')


@router.message(Command("delete_all"))
async def command_delete_all_phrases(message: types.Message):
    await update_last_activity(message)
    await delete_all_data_from_phrases(message.from_user.id)
    await message.answer('✅ You deleted all phrases successful')


@router.message(F.text)
async def spam(message: types.Message):
    await update_last_activity(message)
    await message.delete()

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButton, InlineKeyboardMarkup


async def kb_for_command_menu():
    kb = [
        [
            KeyboardButton(text='📓 Learning'),
            KeyboardButton(text='📨 Add text'),
        ],
        [
            KeyboardButton(text='🎲 Change days before repetition')
        ],
        [
            KeyboardButton(text='🧾 List of phrases'),
            KeyboardButton(text='✂️ Delete phrase'),
        ],
    ]

    client_buttons = ReplyKeyboardMarkup(
        keyboard=kb, resize_keyboard=True, one_time_keyboard=True)

    return client_buttons

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove


async def kb_for_command_menu():
    buttons = [
        [
            KeyboardButton(text='📓 Learning'),
            KeyboardButton(text='📨 Addition'),
        ],
        [
            KeyboardButton(text='🎲 Change days before repetition'),
        ],
        [
            KeyboardButton(text='🧾 List of phrases'),
            KeyboardButton(text='✂️ Deletion'),
        ],
    ]

    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons, one_time_keyboard=True, resize_keyboard=True)

    return keyboard


async def kb_for_delete():
    buttons = [
        [
            InlineKeyboardButton(
                text='Delete all', callback_data='delete_all'),
            InlineKeyboardButton(text='Delete several',
                                 callback_data='delete_several'),
            InlineKeyboardButton(
                text='Delete one', callback_data='delete_one'),
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def kb_for_add():
    buttons = [
        [
            InlineKeyboardButton(
                text='Keyboard with commands', callback_data='keyboard_with_commands'),
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def kb_for_change():
    buttons = [
        [
            InlineKeyboardButton(text='Change by days',
                                 callback_data='change_by_days'),
            InlineKeyboardButton(text='Change several',
                                 callback_data='change_several'),
            InlineKeyboardButton(
                text='Change one', callback_data='change_one'),
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

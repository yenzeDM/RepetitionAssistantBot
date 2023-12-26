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
            InlineKeyboardButton(text='Delete one', callback_data='delete_one')
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def kb_for_add():
    buttons = [
        [
            InlineKeyboardButton(text='Menu', callback_data='menu'),
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

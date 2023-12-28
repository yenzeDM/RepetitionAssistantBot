from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StatesGroup, State
from aiogram import types
from db.func_for_db import show_finished_text_to_repeat, change_date
from additional_func import change_list_output
from asyncio import sleep
from language.russian import Russian


router = Router()


class LearnPhrases(StatesGroup):
    learn = State()


@router.message(F.text.contains('Learning'))
async def learn_handler(message: types.Message, state: FSMContext):
    await state.update_data(text_to_repeat=await show_finished_text_to_repeat(message.from_user.id))
    data = await state.get_data()
    if data['text_to_repeat']:
        await state.set_state(LearnPhrases.learn)
        if len(data['text_to_repeat']) > 100:
            tmp = data['text_to_repeat'].copy()
            await message.answer(Russian.LEARN_NEED)
            await sleep(0.5)
            while tmp:
                await message.answer(await change_list_output(tmp[0:99], help_text=True))
                await sleep(0.5)
                tmp = tmp[99::]
            await text_to_repeat_handler(message, state)
        else:
            tmp = data['text_to_repeat'].copy()
            await message.answer(f'{Russian.LEARN_NEED}\n\n{await change_list_output(tmp, help_text=True)}')
            await sleep(0.5)
            await text_to_repeat_handler(message, state)
    else:
        await message.answer(Russian.LEARN_EMPTY)
        await state.clear()


async def text_to_repeat_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if data['text_to_repeat']:
        await message.answer(f"{data['text_to_repeat'][0][1]}\n\n{Russian.LEARN_TEXT_TO_REPEAT}")
        await state.set_state(LearnPhrases.learn)
    else:
        await message.answer(Russian.FINISH_LEARN_TEXT_TO_REPEAT)
        await state.clear()


@router.message(LearnPhrases.learn)
async def text_validation_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if str(data['text_to_repeat'][0][0]).strip().lower() == message.text.strip().lower():
        await change_date(data['text_to_repeat'][0], message)
        await state.update_data(text_to_repeat=data['text_to_repeat'][1::])
        await message.answer(Russian.LEARN_TEXT_TO_REPEAT_POSITIVE)
        await sleep(0.5)
        await text_to_repeat_handler(message, state)
    else:
        await message.answer(Russian.LEARN_TEXT_TO_REPEAT_NEGATIVE)
        await sleep(0.5)
        await text_to_repeat_handler(message, state)

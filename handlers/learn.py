from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StatesGroup, State
from aiogram import types
from db.func_for_db import update_last_activity, show_phrase_for_learn, change_date_for_phrase
from additional_func import handler_for_show_list
from asyncio import sleep


router = Router()


class LearnPhrases(StatesGroup):
    learn_phrase = State()


@router.message(F.text.contains('Learning'))
async def find_phrases_for_learn(message: types.Message, state: FSMContext):
    await update_last_activity(message)
    await state.update_data(phrases_to_learn=await show_phrase_for_learn(message.from_user.id))
    data = await state.get_data()
    if data['phrases_to_learn']:
        await state.set_state(LearnPhrases.learn_phrase)
        if len(data['phrases_to_learn']) > 100:
            tmp = data['phrases_to_learn'].copy()
            await message.answer(f'To cancel command, you should enter⚠️ /cancel\n\n🧾 Today you need repeat:')
            await sleep(0.5)
            while tmp:
                await message.answer(await handler_for_show_list(tmp[0:99], translation=True))
                await sleep(0.5)
                tmp = tmp[99::]
            await translation(message, state)
        else:
            tmp = data['phrases_to_learn'].copy()
            await message.answer(f'To cancel command, you should enter⚠️ /cancel\n\n🧾 Today you need repeat:\n\n{await handler_for_show_list(tmp, translation=True)}')
            await sleep(0.5)
            await translation(message, state)
    else:
        await message.answer('You have nothing for repetition 🗑')
        await state.clear()


async def translation(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if data['phrases_to_learn']:
        await message.answer(f"{data['phrases_to_learn'][0][1]}\n\n🖌 Enter the answer:")
        await state.set_state(LearnPhrases.learn_phrase)
    else:
        await message.answer("That's all for today 👏")
        await state.clear()


@router.message(LearnPhrases.learn_phrase)
async def learn_text(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if str(data['phrases_to_learn'][0][0]).strip().lower() == message.text.strip().lower():
        await change_date_for_phrase(data['phrases_to_learn'][0], message)
        await state.update_data(phrases_to_learn=data['phrases_to_learn'][1::])
        await message.answer('✅ Your answer is right')
        await sleep(0.5)
        await translation(message, state)
    else:
        await message.answer('❌ Your answer is wrong')
        await sleep(0.5)
        await translation(message, state)

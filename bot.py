import asyncio
from handlers import change_days, other, add, delete, learn, cancel
from db.func_for_db import db_start, db_finish
import logging
from create_bot import dp, bot
from db.func_for_db import get_users_activity, delete_all_user_data, show_phrase_for_learn
import threading
import datetime


async def start_check_user_activity():
    threading.Timer(604800.0, start_check_user_activity).start()
    users_activity = await get_users_activity()
    todays_date = datetime.datetime.strptime(
        str(datetime.date.today()), '%Y-%m-%d')
    for user_id, last_activity in users_activity:
        tmp = datetime.datetime.strptime(last_activity, '%Y-%m-%d')
        days_gone_by = todays_date - tmp
        if days_gone_by.days >= 150:
            await delete_all_user_data(user_id)
        if len(await show_phrase_for_learn(user_id)) > 10:
            await bot.send_message(
                user_id, "🔔 You have more than 10 repetitions, It is time to repeat!")


logging.basicConfig(level=logging.INFO)


async def main():
    print("Bot is turned on")
    db_start()

    dp.include_routers(
        cancel.router,
        add.router,
        delete.router,
        learn.router,
        change_days.router,
        other.router,
    )

    await start_check_user_activity()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, none_stop=True)
    db_finish()
    print("Bot is turned off")


if __name__ == "__main__":
    asyncio.run(main())

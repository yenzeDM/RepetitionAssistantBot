import asyncio
from handlers import change_days, other, add, delete, learn, cancel
from db.func_for_db import db_start, db_finish, get_users_activity, delete_all_user_data, show_finished_text_to_repeat, get_users_id
import logging
from create_bot import dp, bot
import threading
import datetime
import asyncio


def remove_inactive_users():
    threading.Timer(604800.0, remove_inactive_users).start()
    users_activity = get_users_activity()
    todays_date = datetime.datetime.strptime(
        str(datetime.date.today(), '%Y-%m-%d'))
    for user_id, last_activity in users_activity:
        tmp = datetime.datetime.strptime(last_activity, '%Y-%m-%d')
        days_gone_by = todays_date - tmp
        if days_gone_by > 90:
            delete_all_user_data(user_id)


async def notification_to_repeat():
    while True:
        users_id = await get_users_id()
        for id in users_id:
            if len(await show_finished_text_to_repeat(id)) > 20:
                await bot.send_message(id, '🔔 You have more than 20 repetitions, It is time to repeat!')
        await asyncio.sleep(86400)


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

    remove_inactive_users()
    await notification_to_repeat()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, none_stop=True)
    db_finish()
    print("Bot is turned off")


if __name__ == "__main__":
    asyncio.run(main())

import asyncio
from handlers import change_days, other, add, delete, learn, cancel
from db.func_for_db import db_start, get_users_activity, delete_all_user_data, get_users_id, show_finished_text_to_repeat
import logging
from create_bot import dp, bot, scheduler
import datetime
import asyncio
from language.russian import Russian


async def remove_inactive_users():
    users_activity = await get_users_activity()
    todays_date = datetime.datetime.strptime(
        str(datetime.date.today()), '%Y-%m-%d')
    for user_id, last_activity in users_activity:
        tmp = datetime.datetime.strptime(last_activity, '%Y-%m-%d')
        days_gone_by = todays_date - tmp
        if days_gone_by.days >= 0:
            await delete_all_user_data(user_id)


async def notification_to_repeat(bot):
    users_id = await get_users_id()
    for id in users_id:
        if len(await show_finished_text_to_repeat(id[0])) >= 20:
            await bot.send_message(id[0], Russian.TIME_TO_REPEAT)


def schedule_jobs():
    scheduler.add_job(remove_inactive_users, 'interval', seconds=604800)
    scheduler.add_job(notification_to_repeat, 'interval',
                      seconds=86400, args=(bot,))


logging.basicConfig(level=logging.INFO)


async def main(scheduler):
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

    await bot.delete_webhook(drop_pending_updates=True)
    schedule_jobs()
    scheduler.start()
    await dp.start_polling(bot, none_stop=True)
    print("Bot is turned off")


if __name__ == "__main__":
    asyncio.run(main(scheduler))

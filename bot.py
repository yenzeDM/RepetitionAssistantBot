import asyncio
from handlers import change_days, other, add, delete, learn, cancel
from db.func_for_db import db_start, db_finish
import logging
from create_bot import dp, bot


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

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, none_stop=True)
    db_finish()
    print("Bot is turned off")


if __name__ == "__main__":
    asyncio.run(main())

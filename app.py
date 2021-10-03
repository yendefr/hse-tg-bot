from datetime import datetime

from aiogram import executor
from handlers import dp

from loader import bot, scheduler
from utils.notify_admins import on_startup_notify
from utils.db.db import DB

db = DB()


async def update_statuses(db):
    await db.update_is_sick_if_expired(datetime.today())
    await db.update_is_vaccinated_if_expired(datetime.today())


def schedule_jobs():
    scheduler.add_job(update_statuses, 'interval', days=1, args=(db,))


async def on_startup(dispatcher):
    await on_startup_notify(dispatcher)
    schedule_jobs()


async def on_shutdown(dp):
    await bot.close()


if __name__ == '__main__':
    scheduler.start()
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)

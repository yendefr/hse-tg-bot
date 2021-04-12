from aiogram import executor
from handlers import dp

from loader import bot
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify

async def on_startup(dispatcher):
    await on_startup_notify(dispatcher)

async def on_shutdown(dp):
    await bot.close()

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)

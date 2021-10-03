import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from utils.db.create_db import create_pool
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from data.config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.MARKDOWN_V2)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
scheduler = AsyncIOScheduler()

# Data Base
loop = asyncio.get_event_loop()
db = loop.run_until_complete(create_pool())

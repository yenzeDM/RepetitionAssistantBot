from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler


load_dotenv()

Token = os.getenv('TOKEN_TEST')
bot = Bot(Token)
dp = Dispatcher()
scheduler = AsyncIOScheduler()

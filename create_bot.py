from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import os


load_dotenv()

Token = os.getenv('TOKEN')
bot = Bot(Token)
dp = Dispatcher()

from aiogram import Bot, Dispatcher
from data import Token
from dotenv import load_dotenv
import os


load_dotenv()

Token = os.getenv('TOKEN')
bot = Bot(Token)
dp = Dispatcher()
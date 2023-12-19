import os

import dotenv
from aiogram import Dispatcher
from aiogram.enums import ParseMode
from flask import Flask

dotenv.load_dotenv()
# Bot token can be obtained via https://t.me/BotFather
TOKEN = os.getenv("BOT_TOKEN")

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()

app = Flask(__name__)
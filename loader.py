import os

import dotenv
from aiogram import Dispatcher

dotenv.load_dotenv()
# Bot token can be obtained via https://t.me/BotFather
TOKEN = os.getenv("BOT_TOKEN")

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()

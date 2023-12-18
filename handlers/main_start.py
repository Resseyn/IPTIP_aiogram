from aiogram.filters import command, CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from data.configs import pic_pathes
from keyboard import start_keyboard
from loader import dp


@dp.message()
async def command_start_handler(message: Message) -> None:
    await message.answer_photo(photo=pic_pathes["start"], caption=f"Привет, {hbold(message.from_user.full_name)}!\nВыбери комикс!", reply_markup=start_keyboard.keyboard)

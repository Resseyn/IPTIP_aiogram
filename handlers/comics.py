from aiogram import F
from aiogram.types import CallbackQuery, InputMedia, InputMediaPhoto
from aiogram.utils.markdown import hbold

from data.configs import pic_pathes
from keyboard import start_keyboard
from keyboard.comic_keyboard_constructor import create_comic_kb
from loader import dp


@dp.callback_query(F.data == "back")
async def main_menu(callback: CallbackQuery):
    send_media = InputMediaPhoto(media=pic_pathes["start"],
                                 caption=f"Привет, {hbold(callback.from_user.full_name)}!\nВыбери комикс!")
    await callback.message.edit_media(media=send_media, reply_markup=start_keyboard.keyboard)


@dp.callback_query(F.data.startswith("comic"))
async def choose_comic_page_callback(callback: CallbackQuery):
    print(callback.data)
    data = callback.data.split(",")
    if len(data) == 1:
        data.append(1)
    else:
        data[1] = int(data[1])
    keyboard = create_comic_kb(data[0], data[1])
    send_media = InputMediaPhoto(media=pic_pathes[data[0]][data[1]],
                                 caption="")
    await callback.message.edit_media(media=send_media, reply_markup=keyboard)

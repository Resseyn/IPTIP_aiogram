from aiogram import F
from aiogram.types import CallbackQuery, InputMediaPhoto

from database.mongo import mongo_comics
from keyboard import start_keyboard
from keyboard.comic_keyboard_constructor import create_comic_list_kb, create_comic_kb
from loader import dp
from utils.base_pics import pic_pathes


@dp.callback_query(F.data == "list")
async def comics_list(callback: CallbackQuery):
    kb = create_comic_list_kb(callback.from_user.id)
    send_media = InputMediaPhoto(media=pic_pathes["start"],
                                 caption="Твои комиксы")
    await callback.message.edit_media(media=send_media, reply_markup=kb)


@dp.callback_query(F.data == "delete")
async def comics_list(callback: CallbackQuery):
    kb = create_comic_list_kb(callback.from_user.id, delete=True)
    send_media = InputMediaPhoto(media=pic_pathes["start"],
                                 caption="Твои комиксы\nАккуратно, если нажмешь на один - сразу его удалишь")
    await callback.message.edit_media(media=send_media, reply_markup=kb)


@dp.callback_query()
async def personal_comic(callback: CallbackQuery):
    result = mongo_comics.find_one({"chat_id": callback.from_user.id})
    data = callback.data.split(",")
    if len(data) == 1:
        data.append("1")
    elif data[1] == "-1":
        await callback.answer(text="Вы удалили комикс, за что(", show_alert=True)
        mongo_comics.update_one({"chat_id": callback.from_user.id}, {'$unset': {data[0]: ""}})
        kb = create_comic_list_kb(callback.from_user.id, delete=True)
        await callback.message.edit_reply_markup(reply_markup=kb)
        return
    comic_dict = result.get(data[0])
    keyboard = create_comic_kb(data[0], comic_dict, data[1])
    send_media = InputMediaPhoto(media=comic_dict[str(int(data[1]) - 1)],
                                 caption="")
    await callback.message.edit_media(media=send_media, reply_markup=keyboard)

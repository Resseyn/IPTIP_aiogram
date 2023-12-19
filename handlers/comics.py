from aiogram import F
from aiogram.filters import Command
from aiogram.types import CallbackQuery, InputMediaPhoto, Message
from aiogram.utils.markdown import hbold

from data.user_interactions import creating_states
from database.mongo import mongo_comics
from keyboard import start_keyboard
from keyboard.comic_keyboard_constructor import create_comic_kb
from loader import dp
from utils.base_pics import pic_pathes


@dp.callback_query(F.data == "back")
async def main_menu(callback: CallbackQuery):
    send_media = InputMediaPhoto(media=pic_pathes["start"],
                                 caption=f"Привет, {hbold(callback.from_user.full_name)}!\nВыбери комикс!")
    await callback.message.edit_media(media=send_media, reply_markup=start_keyboard.keyboard)


@dp.callback_query(F.data.startswith("comic"))
async def choose_comic_page_callback(callback: CallbackQuery):
    data = callback.data.split(",")
    if len(data) == 1:
        data.append("1")
    keyboard = create_comic_kb(data[0], pic_pathes[data[0]], data[1])
    send_media = InputMediaPhoto(media=pic_pathes[data[0]][str(int(data[1]) - 1)],
                                 caption="")
    await callback.message.edit_media(media=send_media, reply_markup=keyboard)


@dp.callback_query(F.data == "create")
async def create_comic(callback: CallbackQuery):
    creating_states[callback.from_user.id] = {"data": []}
    send_media = InputMediaPhoto(media=pic_pathes["start"],
                                 caption=f"Введи название нового комикса")
    await callback.message.edit_media(media=send_media)


@dp.message(Command("end"))
async def photo_for_comics_handler(message: Message):
    if len(creating_states[message.from_user.id]["data"]) <= 2:
        await message.answer_photo(photo=pic_pathes["start"],
                                   caption="Вы добавили слишком мало картинок!\nОтправьте минимум две картинки")
    else:
        new_comic = {}
        for index, file_id in enumerate(creating_states[message.from_user.id]["data"][1:]):
            new_comic[str(index)] = file_id

        filter_dict = {"chat_id": message.from_user.id}

        result = mongo_comics.find_one(filter_dict)

        if result is not None:
            mongo_comics.update_one(filter=filter_dict,
                                    update={"$set": {str(creating_states[message.from_user.id]["data"][0]): new_comic}})
        else:
            dict_for_mongo = {
                "chat_id": message.from_user.id,
                str(creating_states[message.from_user.id]["data"][0]): new_comic
            }
            mongo_comics.insert_one(dict_for_mongo)

        await message.answer_photo(photo=pic_pathes["start"],
                                   caption=f"Комикс {creating_states[message.from_user.id]['data'][0]} создан!")
        creating_states.pop(message.from_user.id)


@dp.message(lambda message: message.from_user.id in creating_states)
async def photo_for_comics_handler(message: Message):
    if (message.text is not None) and (message.photo is None) and len(
            creating_states[message.from_user.id]["data"]) == 0:
        if len(message.text) < 30:
            creating_states[message.from_user.id]["data"].append(message.text)
            await message.answer_photo(photo=pic_pathes["start"],
                                       caption=f"Отлично, комикс - {message.text}\nНачинай отправлять содержание "
                                               f"комикса\n" +
                                               f"Пропиши /end для сохранения результата")
        else:
            await message.answer_photo(photo=pic_pathes["start"],
                                       caption="Слишком большое название!")
    elif message.text is None and message.photo is not None and len(creating_states[message.from_user.id]["data"]) != 0:
        creating_states[message.from_user.id]["data"].append(message.photo[-1].file_id)
    else:
        await message.answer_photo(photo=pic_pathes["start"],
                                   caption="Сначала введи название!")

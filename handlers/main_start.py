from aiogram import F
from aiogram.filters import command, CommandStart
from aiogram.types import Message, InputMediaPhoto
from aiogram.utils.markdown import hbold
from sqlalchemy.orm import sessionmaker

import keyboard.start_keyboard
from data.orm_classes import Student
from data.user_interactions import register_states
from database.postgres import engine, session, students
from helpers.funcs import format_russian_phone_number, is_valid_group_number
from keyboard import start_keyboard
from loader import dp
from utils.base_pics import pic_pathes


@dp.message(lambda message: message.from_user.id in register_states and register_states[message.from_user.id]["stage"] == 1)
async def stage_1_register_handler(message: Message):
    if message.text is not None:
        if message.text.find(" ") == -1:
            await message.answer_photo(photo=pic_pathes["start"],
                                       caption="Ты все неправильно ввел!!!")
        else:
            surname, name = message.text.split(" ")
            register_states[message.from_user.id]["stage"] += 1
            register_states[message.from_user.id]["data"].append(surname)
            register_states[message.from_user.id]["data"].append(name)
            print(register_states[message.from_user.id])
            await message.answer_photo(photo=pic_pathes["start"],
                                         caption="Отлично, а теперь введи свой номер телефона")


@dp.message(lambda message: message.from_user.id in register_states and register_states[message.from_user.id]["stage"] == 2)
async def stage_2_register_handler(message: Message):
    if message.text is not None:
        number = format_russian_phone_number(message.text)
        if number == "Неверный формат номера":
            await message.answer_photo(photo=pic_pathes["start"],
                                       caption="Неверный формат номера\nВведи свой номер телефона правильно")
        else:
            register_states[message.from_user.id]["stage"] += 1
            register_states[message.from_user.id]["data"].append(number)
            await message.answer_photo(photo=pic_pathes["start"],
                                   caption="Отлично, а теперь введи свою группу и институт в формате: ЭФБО-03-23 ИПТИП")

@dp.message(lambda message: message.from_user.id in register_states and register_states[message.from_user.id]["stage"] == 3)
async def stage_3_register_handler(message: Message):
    if message.text is not None:
        if message.text.find(" ") == -1:
            await message.answer_photo(photo=pic_pathes["start"],
                                       caption="Ты все неправильно ввел!!!")
        else:
            group, institution = message.text.split(" ")
            if not(is_valid_group_number(group)):
                await message.answer_photo(photo=pic_pathes["start"],
                                           caption="Ты неправильно ввел свою группу!")
            elif len(institution) >= 10:
                await message.answer_photo(photo=pic_pathes["start"],
                                           caption="Ты неправильно ввел свой институт!")
            else:
                register_states[message.from_user.id]["data"].append(group)
                register_states[message.from_user.id]["data"].append(institution)
                new_student = Student(
                    telegram_nickname="@" + message.from_user.username,
                    surname=register_states[message.from_user.id]["data"][0],
                    name=register_states[message.from_user.id]["data"][1],
                    telephone_number=register_states[message.from_user.id]["data"][2],
                    group=register_states[message.from_user.id]["data"][3],
                    institution=register_states[message.from_user.id]["data"][4],
                    status='ACTIVE',
                    tg_chat_id = message.from_user.id,
                )
                session.add(new_student)
                session.commit()
                register_states.pop(message.from_user.id)
                await message.answer_photo(photo=pic_pathes["start"],
                                           caption="Отлично, ты прошел регистрацию!\nМожешь выбрать комикс!",
                                           reply_markup=start_keyboard.keyboard)


@dp.message()
async def command_start_handler(message: Message) -> None:
    if session.query(students).filter_by(tg_chat_id=message.from_user.id).first() is None:
        register_states[message.from_user.id] = {"stage": 1, "data": []}
        await message.answer_photo(photo=pic_pathes["start"],
                                   caption=f"Привет, {hbold(message.from_user.full_name)}!\nЭто начало регистрации\nВведи свою фамилию и имя", )
    else:
        await message.answer_photo(photo=pic_pathes["start"],
                               caption=f"Привет, {hbold(message.from_user.full_name)}!\nВыбери комикс!",
                               reply_markup=start_keyboard.keyboard)

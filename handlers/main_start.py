from aiogram import F
from aiogram.filters import command, CommandStart
from aiogram.types import Message, InputMediaPhoto
from aiogram.utils.markdown import hbold
from sqlalchemy.orm import sessionmaker

from data.configs import pic_pathes
from data.orm_classes import Student
from data.user_interactions import user_states
from database.database import engine, session, students
from helpers.funcs import format_russian_phone_number, is_valid_group_number
from keyboard import start_keyboard
from loader import dp



@dp.message(lambda message: message.from_user.id in user_states and user_states[message.from_user.id]["stage"] == 1)
async def stage_1_register_handler(message: Message):
    if message.text.find(" ") == -1:
        await message.answer_photo(photo=pic_pathes["start"],
                                   caption="Ты все неправильно ввел!!!")
    else:
        surname, name = message.text.split(" ")
        user_states[message.from_user.id]["stage"] += 1
        user_states[message.from_user.id]["data"].append(surname)
        user_states[message.from_user.id]["data"].append(name)
        print(user_states[message.from_user.id])
        await message.answer_photo(photo=pic_pathes["start"],
                                     caption="Отлично, а теперь введи свой номер телефона")


@dp.message(lambda message: message.from_user.id in user_states and user_states[message.from_user.id]["stage"] == 2)
async def stage_2_register_handler(message: Message):
    number = format_russian_phone_number(message.text)
    if number == "Неверный формат номера":
        await message.answer_photo(photo=pic_pathes["start"],
                                   caption="Неверный формат номера\nВведи свой номер телефона правильно")
    else:
        user_states[message.from_user.id]["stage"] += 1
        user_states[message.from_user.id]["data"].append(number)
        await message.answer_photo(photo=pic_pathes["start"],
                               caption="Отлично, а теперь введи свою группу и институт в формате: ЭФБО-03-23 ИПТИП")

@dp.message(lambda message: message.from_user.id in user_states and user_states[message.from_user.id]["stage"] == 3)
async def stage_3_register_handler(message: Message):
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
            user_states[message.from_user.id]["data"].append(group)
            user_states[message.from_user.id]["data"].append(institution)
            new_student = Student(
                telegram_nickname="@" + message.from_user.username,
                surname=user_states[message.from_user.id]["data"][0],
                name=user_states[message.from_user.id]["data"][1],
                telephone_number=user_states[message.from_user.id]["data"][2],
                group=user_states[message.from_user.id]["data"][3],
                institution=user_states[message.from_user.id]["data"][4],
                status='ACTIVE',
                tg_chat_id = message.from_user.id,
            )
            session.add(new_student)
            session.commit()
            user_states.pop(message.from_user.id)
            await message.answer_photo(photo=pic_pathes["start"],
                                       caption="Отлично, ты прошел регистрацию!\nМожешь выбрать комикс!")


@dp.message()
async def command_start_handler(message: Message) -> None:
    if session.query(students).filter_by(tg_chat_id=message.from_user.id).first() is None:
        user_states[message.from_user.id] = {"stage": 1, "data": []}
        await message.answer_photo(photo=pic_pathes["start"],
                                   caption=f"Привет, {hbold(message.from_user.full_name)}!\nЭто начало регистрации\nВведи свою фамилию и имя", )
    # id = message.photo[-1].file_id
    # file = await bot.get_file(file_id)
    # url = bot.get_file_url(file.file_path) #TODO: для второго таска
    # TODO: не забыть спрашивать юзера когда он хочет удалить комикс
    else:
        await message.answer_photo(photo=pic_pathes["start"],
                               caption=f"Привет, {hbold(message.from_user.full_name)}!\nВыбери комикс!",
                               reply_markup=start_keyboard.keyboard)

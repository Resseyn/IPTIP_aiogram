from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from data.configs import pic_pathes

# Функция для формирования инлайн-клавиатуры на лету
page_text = {
    0: "Назад",
    1: "Вперед",
}


def create_comic_kb(type: str, page=1) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []

    for i in range(-1, 3, 2):
        if page == 1 and i == -1:
            continue
        elif page == len(pic_pathes[type]) and i == 1:
            continue
        buttons.append(InlineKeyboardButton(
            text=page_text[(i + 1) // 2],
            callback_data= type + "," + str(page + i)
        ))
    buttons.append(InlineKeyboardButton(
        text="Вернуться к комиксам",
        callback_data="back"))

    kb_builder.row(*buttons, width=1 if len(buttons) == 2 else 2)

    return kb_builder.as_markup()

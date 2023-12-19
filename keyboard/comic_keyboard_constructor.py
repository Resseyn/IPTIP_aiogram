from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.mongo import mongo_comics

page_text = {
    0: "Назад",
    1: "Вперед",
}


def create_comic_kb(comic_type: str, comic_dict: dict, page="1") -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    page = int(page)
    for i in range(-1, 3, 2):
        if page == 1 and i == -1:
            continue
        elif page == len(comic_dict) and i == 1:
            continue
        buttons.append(InlineKeyboardButton(
            text=page_text[(i + 1) // 2],
            callback_data=comic_type + "," + str(page + i)
        ))
    buttons.append(InlineKeyboardButton(
        text="Вернуться к комиксам",
        callback_data="back"))

    kb_builder.row(*buttons, width=1 if len(buttons) == 2 else 2)

    return kb_builder.as_markup()


def create_comic_list_kb(chat_id: int, delete=False):
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    result = mongo_comics.find_one({"chat_id": chat_id})
    if result is None:
        buttons.append(InlineKeyboardButton(
            text="Вернуться к комиксам",
            callback_data="back"))
        kb_builder.row(*buttons, width=1 if len(buttons) == 2 else 2)
        return kb_builder.as_markup()
    else:
        for key, value in result.items():
            if key != "chat_id" and key != "_id":
                buttons.append(InlineKeyboardButton(
                    text=key,
                    callback_data=key + (",-1" if delete else ""),
                ))
        kb_builder.row(*buttons,
                       width=1 if len(buttons) >= 6 else 2)  # TODO: повторить подвиг вывода данных как со сниппетами
        kb_builder.row(InlineKeyboardButton(
            text="Вернуться к комиксам",
            callback_data="back"))
        return kb_builder.as_markup()

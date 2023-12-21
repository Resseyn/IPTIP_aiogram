# Создаем объекты инлайн-кнопок
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

big_button_0 = InlineKeyboardButton(
    text='Открыть сайт',
    web_app=WebAppInfo(url="https://lk.mirea.ru/"),
)

big_button_1 = InlineKeyboardButton(
    text='Комикс 1',
    callback_data='comic_1'
)

big_button_2 = InlineKeyboardButton(
    text='Комикс 2',
    callback_data='comic_2'
)
big_button_3 = InlineKeyboardButton(
    text='Оригинальнейший комикс',
    callback_data='comic_3'
)
big_button_4 = InlineKeyboardButton(
    text='Создать комикс',
    callback_data='create'
)
big_button_5 = InlineKeyboardButton(
    text='Мои комиксы',
    callback_data='list'
)
big_button_6 = InlineKeyboardButton(
    text='Удаление моих комиксов(',
    callback_data='delete'
)

keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[big_button_0],
                     [big_button_1],
                     [big_button_2],
                     [big_button_3],
                     [big_button_4],
                     [big_button_5],
                     [big_button_6]]
)

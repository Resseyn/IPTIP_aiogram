# Создаем объекты инлайн-кнопок
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

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

keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[big_button_1],
                     [big_button_2],
                     [big_button_3]]
)
import re

def format_russian_phone_number(phone_number):
    # Удаляем все нецифровые символы
    digits = re.sub(r'\D', '', phone_number)

    # Проверяем, что номер начинается с 7 или 8 и содержит 11 цифр
    if not re.match(r'^(?:\+?7|8)\d{10}$', digits):
        return "Неверный формат номера"

    # Заменяем начальную 8 на 7
    if digits.startswith('+'):
        digits = "7" + digits[2:]
    elif digits.startswith('8'):
        digits = '7' + digits[1:]

    # Форматируем номер в формат +7 123 456-78-90
    formatted_number = '+{} {} {}-{}-{}'.format(digits[0:1], digits[1:4], digits[4:7], digits[7:9], digits[9:])

    return formatted_number

def is_valid_group_number(group_number):
    pattern = r'^\w{2}БО-\d{2}-\d{2}$'
    return bool(re.match(pattern, group_number))



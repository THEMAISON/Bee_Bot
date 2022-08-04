order_id = {
    'Предмет': '1',
    'Семестр': '1',
    'Задание': '1',
    'Номер': '0',
    'Вариант': '0',
    'Условие': '',
    'Пожелание': '',
    'Услуга': '1',
}

order_convert = {
    'Предмет': {
        '1': 'АИП',
        '2': 'ООП',
        '3': 'ООП',
    },
    'Семестр': {
        '1': 'I',
        '2': 'II',
        '3': 'III',
        '4': 'IV',
    },
    'Задание': {
        '1': 'Лаба',
        '2': 'Функция',
        '3': 'РГР',
        '4': 'Практика',
    },
    'Услуга': {
        '1': 'Отчет',
        '2': 'Код',
    },
}

flags = {
    'wish': False,
    'condition': False
}


def get_order():
    order_text = ''
    for key, value in order_id.items():
        if key in 'ПредметСеместрЗаданиеУслуга':
            order_text += f'▫ *{key}*: {order_convert.get(key).get(value)}\n'
        elif value not in ' 0':
            order_text += f'▫ *{key}*: {value}\n'
    return order_text

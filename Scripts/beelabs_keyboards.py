from aiogram import types

count_labs = {
    1: 7,
    2: 8,
    3: 9,
    4: 10,
}

cancel_button = types.InlineKeyboardButton('❌ Отменить', callback_data='cancel')

conditions = types.InlineKeyboardMarkup(row_width=2)
send_condition = types.InlineKeyboardButton('📤 Отправить', callback_data='condition')
conditions.add(cancel_button, send_condition)

wishes = types.InlineKeyboardMarkup(row_width=2)
send_wish = types.InlineKeyboardButton('📤 Отправить', callback_data='wish')
wishes.add(cancel_button, send_wish)

confirmation_start = types.InlineKeyboardMarkup(row_width=2)
ready = types.InlineKeyboardButton('✏ Начать', callback_data='ready')
confirmation_start.add(cancel_button, ready)

class_names = types.InlineKeyboardMarkup(row_width=3)
aip = types.InlineKeyboardButton('АИП', callback_data='class_name1')
# oop = types.InlineKeyboardButton('ООП', callback_data='class_name2')
# occ = types.InlineKeyboardButton('ОСС', callback_data='class_name3')
class_names.add(aip)
class_names.add(cancel_button)

semester_nums = types.InlineKeyboardMarkup(row_width=4)
sem1 = types.InlineKeyboardButton('I Семестр', callback_data='semester1')
sem2 = types.InlineKeyboardButton('II Семестр', callback_data='semester2')
# sem3 = types.InlineKeyboardButton('III Семестр', callback_data='semester3')
# sem4 = types.InlineKeyboardButton('IV Семестр', callback_data='semester4')
semester_nums.add(sem1, sem2)
semester_nums.add(cancel_button)

tasks = types.InlineKeyboardMarkup(row_width=4)
laba = types.InlineKeyboardButton('⚗ Лаба', callback_data='task1')
fun = types.InlineKeyboardButton('⚙ Функция', callback_data='task2')
# rgr = types.InlineKeyboardButton('📜 РГР', callback_data='task3')
# practice = types.InlineKeyboardButton('⚒ Практика', callback_data='task4')
tasks.add(laba, fun)
tasks.add(cancel_button)


def set_markup(prefix, markup, count_buttons):
    cb = 0
    for i in range(1, 9):
        for j in range(1, 9):
            cb += 1
            text = str(j + (i - 1) * 8)
            button = types.InlineKeyboardButton(text, callback_data=f'{prefix}{text}')
            if j == 1:
                markup.add(button)
            else:
                markup.insert(button)
            if cb == count_buttons:
                markup.add(cancel_button)
                return markup


def get_laba_nums(count_nums):
    laba_nums = types.InlineKeyboardMarkup(row_width=8)
    laba_nums = set_markup('laba', laba_nums, count_labs.get(count_nums))
    return laba_nums


variants = types.InlineKeyboardMarkup(row_width=8)
variants = set_markup('variant', variants, 30)

way_releases = types.InlineKeyboardMarkup(row_width=2)
doc = types.InlineKeyboardButton('📑 Отчёт', callback_data='way_release1')
code = types.InlineKeyboardButton('⌨ Код', callback_data='way_release2')
way_releases.add(doc, code)
way_releases.add(cancel_button)

confirmation_end = types.InlineKeyboardMarkup(row_width=2)
confirm = types.InlineKeyboardButton('✅ Подтвердить', callback_data='confirm')
cancel = types.InlineKeyboardButton('❌ Отменить', callback_data='cancel')
confirmation_end.add(cancel, confirm)

web_site = types.InlineKeyboardMarkup()
site = types.InlineKeyboardButton('Перейти', 'https://vk.com/the_maison')
web_site.add(site)

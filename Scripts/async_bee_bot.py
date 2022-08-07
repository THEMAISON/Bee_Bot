import logging
import schedule
from aiogram import Bot, Dispatcher, executor, types
from configure import config, path, group_id
from beelabs_values import order_id, get_order, flags
from autolocation import identify_location, coordinates
from beelabs_keyboards import confirmation_start, class_names, semester_nums, tasks, get_laba_nums, variants, \
    way_releases, confirmation_end, web_site, conditions, wishes

API_TOKEN = config.get('token')

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message) -> None:
    await message.answer('🐝 *Bee Bot* - Бот для студентов СЕВГУ\n'
                         '🛠 *Разработчик* - THEMAISON',
                         parse_mode='MARKDOWN')
    await message.delete()


@dp.message_handler(commands=['links'])
async def send_welcome(message: types.Message) -> None:
    links = types.InlineKeyboardMarkup(row_width=2)
    sevsu = types.InlineKeyboardButton('🌊 SevSU', 'https://www.sevsu.ru/')
    moodle = types.InlineKeyboardButton('🖥 Moodle', 'https://do.sevsu.ru/')
    rocket = types.InlineKeyboardButton('📢 Rocket Chat', 'https://chat.is.sevsu.ru/')
    links.add(sevsu)
    links.add(moodle, rocket)
    await message.answer('🔗 Доступные ссылки', reply_markup=links)
    await message.delete()


@dp.message_handler(commands=['sdoc'])
async def get_schedule_document(message: types.Message) -> None:
    if schedule.check_for_updates() or not schedule.have_legacy():
        schedule.download()
        await message.answer('✅ Расписание обновлено')

    iituts = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    is1 = types.KeyboardButton('📗 ИС1')
    is2 = types.KeyboardButton('📕 ИС2')
    is3 = types.KeyboardButton('📘 ИС3')
    pi1 = types.KeyboardButton('📙 ПИ1')
    iituts.add(is1, is2, is3, pi1)

    await message.delete()
    await message.answer('🐝 Выберите вашу группу', reply_markup=iituts)


@dp.message_handler(commands=['beelabs'])
async def get_beelabs(message: types.Message) -> None:
    await message.delete()
    await bot.send_message(message.from_user.id, '📝 Начать оформление заказа?', reply_markup=confirmation_start)


@dp.message_handler(content_types=['text'])
async def message_answers(message: types.Message) -> None:
    if flags.get('wish'):
        order_id['Пожелание'] += f'{message.text} '
        await message.delete()

    elif flags.get('condition'):
        order_id['Условие'] += f'{message.text} '
        await message.delete()

    elif 'ИС' in message.text or 'ПИ' in message.text:
        group = int(message.text[-1]) if 'ИС' in message.text else 4

        if schedule.create_new_schedule(group):
            await message.answer(
                f'📚 *Расписание*\n'
                f'Группа: *{schedule.get_file_name(group)}*\n'
                f'Текущая неделя: *{str(schedule.current_week())}*',
                reply_markup=types.ReplyKeyboardRemove())

            with open(path.get('schedules') + schedule.get_file_name(group) + '.xlsx', 'rb') as new_schedule:
                await bot.send_document(message.chat.id, new_schedule)
        else:
            await message.answer('⚠ Расписание недоступно!', reply_markup=types.ReplyKeyboardRemove())

    if message.text.startswith('!'):
        identify_location(message.text[1:])
        await bot.send_location(message.chat.id, coordinates.get('latitude'), coordinates.get('longitude'))

    elif message.text.lower() == 'пчела?':
        await message.answer('Долбаёб?')

    elif 'даня' in message.text.lower() and message.chat.id == group_id.get('student_sevsu'):
        await bot.send_sticker(message.chat.id,
                               sticker='CAACAgIAAxkBAAEFcAABYugSXfOM5JcRtFHssaSjrJPqjvsAAoUaAALJNVFImYmO43hfnoUpBA',
                               reply_to_message_id=message.message_id)


@dp.callback_query_handler()
async def beelabs_callback(callback: types.CallbackQuery) -> None:
    if callback.data == 'ready':
        await beelabs_message(callback, 'Отлично! Переходим к оформлению заказа', '📒 Выберите тип предмета', class_names)

    elif 'class_name' in callback.data:
        order_id['Предмет'] = callback.data[-1]
        await beelabs_message(callback, 'Предмет выбран!', '🎓 Выберите семестр', semester_nums)

    elif 'semester' in callback.data:
        order_id['Семестр'] = callback.data[-1]
        await beelabs_message(callback, 'Семестр выбран!', '🏗 Выберите тип задания', tasks)

    elif 'task' in callback.data:
        task_type = callback.data[-1]
        order_id['Задание'] = task_type

        if task_type == '1':
            await beelabs_message(callback, 'Задание выбрано!', '⚗ Выберите номер лабораторной работы',
                                  get_laba_nums(int(order_id.get('Семестр'))))
        elif task_type in '2':
            flags['condition'] = True
            await beelabs_message(callback, 'Задание выбрано!', '✒ Напишите условие', conditions)

    elif 'laba' in callback.data:
        order_id['Номер'] = callback.data[4:]
        await beelabs_message(callback, 'Номер выбран!', '⚗ Выберите вариант', variants)

    elif 'variant' in callback.data:
        order_id['Вариант'] = callback.data[7:]
        await beelabs_message(callback, 'Вариант выбран!', '📦 Выберите тип услуги', way_releases)

    elif 'way_release' in callback.data:
        order_id['Услуга'] = callback.data[-1]
        flags['wish'] = True
        await beelabs_message(callback, 'Услуга выбрана!', '💡 Напишите пожелание (необязательно)', wishes)

    elif 'condition' in callback.data:
        flags['condition'] = False
        await beelabs_message(callback, 'Условие отправлено!', '📦 Выберите тип услуги', way_releases)

    elif 'wish' in callback.data:
        flags['wish'] = False
        await beelabs_message(callback, 'Пожелание отправлено!', f'🛒 Подтвердите ваш заказ\n{get_order()}',
                              confirmation_end)

    elif callback.data == 'confirm':
        order_id['Условие'] = ''
        order_id['Пожелание'] = ''
        await beelabs_message(callback, 'Почти готово!', '📲 Перейдите на сайт', web_site)

    elif callback.data == 'cancel':
        order_id['Условие'] = ''
        order_id['Пожелание'] = ''
        await callback.answer('Заказ отменен!')
        await callback.message.delete()


async def beelabs_message(callback, answer_text, message_text, markup) -> None:
    await callback.answer(answer_text)
    await callback.message.edit_text(message_text, parse_mode='MARKDOWN')
    await callback.message.edit_reply_markup(markup)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

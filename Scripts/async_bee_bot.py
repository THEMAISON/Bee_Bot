from aiogram import Bot, Dispatcher, executor, types
from autolocation import *
from schedule_receipt import prepare
from file_names import schedules
from configure import config

bot = Bot(token=config['token'])
dp = Dispatcher(bot)

is_schedule = False


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message) -> None:
    await message.answer('🐝 *Bee Bot* - Бот для студентов СЕВГУ\n🛠 *Разработчик* - THEMAISON', parse_mode='MARKDOWN')
    await message.delete()


@dp.message_handler(commands=['links'])
async def send_welcome(message: types.Message) -> None:
    links = types.InlineKeyboardMarkup(row_width=3)
    sevsu = types.InlineKeyboardButton('🌊 Оф. Сайт', 'https://www.sevsu.ru/')
    moodle = types.InlineKeyboardButton('💻 Мудл', 'https://do.sevsu.ru/')
    rocket = types.InlineKeyboardButton('📢 Рокет Чат', 'https://chat.is.sevsu.ru/')
    elective = types.InlineKeyboardButton('🎽 Электив Физ-ра', 'https://elective.sevsu.ru/dashboard')
    links.add(sevsu)
    links.add(moodle, rocket, elective)
    await message.answer('🔗 Доступные ссылки', reply_markup=links)
    await message.delete()


@dp.message_handler(commands=['sch'])
async def get_main_schedule(message: types.Message) -> None:
    sch = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    m = types.KeyboardButton('📖 Основное')
    n = types.KeyboardButton('📒 Новое')
    p = types.KeyboardButton('📓 ПУЛ')
    sch.add(m, n, p)
    await message.delete()
    await message.answer('Выберите раписание...', reply_markup=sch)
    global is_schedule
    is_schedule = True


@dp.message_handler(commands=['beelabs'])
async def get_beelabs(message: types.Message) -> None:
    links = types.InlineKeyboardMarkup(row_width=1)
    bee_labs = types.InlineKeyboardButton('🐝 BEELABS', 'https://vk.com')
    links.add(bee_labs)
    await message.answer('🔗 Доступные ссылки', reply_markup=links)
    await message.delete()


@dp.message_handler(content_types=['text'])
async def message_answers(message: types.Message) -> None:
    global is_schedule
    if is_schedule:
        await message.answer(f'*✅ Расписание готово*\n', parse_mode='MARKDOWN')

        for key, value in schedules.items():
            if message.text[2:] in value:
                with open(prepare(key), 'rb') as file:
                    await bot.send_document(message.chat.id, file, reply_markup=types.ReplyKeyboardRemove())
                break

        is_schedule = False

    elif message.text.startswith('!'):
        identify_location(message.text[1:])
        await bot.send_location(message.chat.id, coordinates['latitude'], coordinates['longitude'])

    elif message.text.lower() == 'пчела?':
        await message.answer('Долбаёб?')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

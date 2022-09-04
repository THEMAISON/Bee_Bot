from aiogram import Bot, Dispatcher, executor, types
from autolocation import *
from schedule_receipt import prepare

API_TOKEN = config.get('token')

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


# await message.answer('✅ Расписание обновлено')
# await message.answer('⚠ Расписание недоступно!)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message) -> None:
    await message.answer('🐝 *Bee Bot* - Бот для студентов СЕВГУ\n🛠 *Разработчик* - THEMAISON', parse_mode='MARKDOWN')
    await message.delete()


@dp.message_handler(commands=['links'])
async def send_welcome(message: types.Message) -> None:
    links = types.InlineKeyboardMarkup(row_width=2)
    sevsu = types.InlineKeyboardButton('🌊 SEVSU', 'https://www.sevsu.ru/')
    moodle = types.InlineKeyboardButton('🖥 MOODLE', 'https://do.sevsu.ru/')
    rocket = types.InlineKeyboardButton('📢 ROCKET', 'https://chat.is.sevsu.ru/')
    links.add(sevsu)
    links.add(moodle, rocket)
    await message.answer('🔗 Доступные ссылки', reply_markup=links)
    await message.delete()


@dp.message_handler(commands=['sch'])
async def get_main_schedule(message: types.Message) -> None:
    schedules = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    m = types.KeyboardButton('🍬 ОСНОВНОЕ')
    p = types.KeyboardButton('🍫 ПУЛ')
    f = types.KeyboardButton('🍿 ФИЗРА')
    schedules.add(m, p, f)
    await message.delete()
    await message.answer('Выберите раписание...', reply_markup=schedules)


@dp.message_handler(commands=['beelabs'])
async def get_beelabs(message: types.Message) -> None:
    links = types.InlineKeyboardMarkup(row_width=1)
    bee_labs = types.InlineKeyboardButton('🐝 BEELABS', 'https://vk.com')
    links.add(bee_labs)
    await message.answer('🔗 Доступные ссылки', reply_markup=links)
    await message.delete()


@dp.message_handler(content_types=['text'])
async def message_answers(message: types.Message) -> None:
    if '🍬 ОСНОВНОЕ' in message.text:
        await message.delete()
        await message.answer(f'*🍬 Основное расписание*\n', parse_mode='MARKDOWN')
        with open(prepare('main'), 'rb') as file:
            await bot.send_document(message.chat.id, file, reply_markup=types.ReplyKeyboardRemove())

    elif '🍫 ПУЛ' in message.text:
        await message.delete()
        await message.answer(f'*🍫 ПУЛ*\n', parse_mode='MARKDOWN')
        with open(prepare('pul'), 'rb') as file:
            await bot.send_document(message.chat.id, file, reply_markup=types.ReplyKeyboardRemove())

    elif '🍿 ФИЗРА' in message.text:
        await message.delete()
        await message.answer('⚠ Расписание недоступно!', reply_markup=types.ReplyKeyboardRemove())

    elif message.text.startswith('!'):
        identify_location(message.text[1:])
        await bot.send_location(message.chat.id, coordinates['latitude'], coordinates['longitude'])

    elif message.text.lower() == 'пчела?':
        await message.answer('Долбаёб?')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

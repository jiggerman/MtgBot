from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from main import add_all_cards_from_file, create_new_client_sheet, add_cards, delete_card, print_all_cards_from_sheet
import time


bot = Bot(token='---', parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_buttons = ['Информация', 'Добавить карты', 'Мои карты']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer('Выберите категорию', reply_markup=keyboard)


@dp.message_handler(Text(equals='Назад'))
async def start(message: types.Message):
    start_buttons = ['Информация', 'Добавить карты', 'Мои карты']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer('Выберите категорию', reply_markup=keyboard)


@dp.message_handler(Text(equals='Добавить карты'))
async def add_card_or_txt(message: types.Message):
    # Создаем новый sheet
    create_new_client_sheet(message.from_user.username)

    start_buttons = ['Добавить карту', 'Файл типа .txt', 'Назад']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer('Выберите категорию', reply_markup=keyboard)


@dp.message_handler(Text(equals='Добавить карту'))
async def add_card(message: types.Message):
    await message.answer('Введите позиции в виде: ссылка кол-во качество')

    @dp.message_handler(content_types=["text"])
    async def minimum(message: types.Message):
        cards = message.text
        result = add_cards(message.from_user.username, cards)
        if result == 1:
            await message.answer('Карты добавлины успешно')
        else:
            await message.answer('При добавлении карты произошла ошибка (проверьте поля ввода)')


@dp.message_handler(Text(equals='Файл типа .txt'))
async def add_cards_from_txt(message: types.Message):
    await message.answer('Ожидаю файл')

    @dp.message_handler(content_types=types.ContentType.DOCUMENT)
    async def download_file(message: types.Message):
        await message.answer('Скачиваю файл...')
        destination = r"C:\Users\ligge\OneDrive\Рабочий стол\Python_Projects_2023\Bot_mtg\Users_files\file.txt"
        await message.document.download(destination)
        result = add_all_cards_from_file(message.from_user.username, destination)
        if result == 1:
            await message.answer('Карты добавлены успешно')
        else:
            await message.answer('При добавлении карт произошла ошибка (проверьте поля ввода)')


@dp.message_handler(Text(equals='Мои карты'))
async def take_cards_from_sheet(message: types.Message):
    start_buttons = ['Распечатать список', 'Проверить наличие карт', 'Удалить карту', 'Назад']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer('Выберите категорию', reply_markup=keyboard)


@dp.message_handler(Text(equals='Распечатать список'))
async def print_list(message: types.Message):
    await message.answer('Собираю информацию...')
    time.sleep(3)

    array = print_all_cards_from_sheet(message.from_user.username)
    await message.answer(f'Найдено {len(array)} карты')
    counter = 0
    for card in array:
        counter += 1
        mes = f'{card[0]} {card[1]} {card[2]}'
        await message.answer(mes)
        if counter == 5:
            time.sleep(3)
            counter = 0


@dp.message_handler(Text(equals='Проверить наличие карт'))
async def is_card_in(message: types.Message):
    await message.answer('Данная функция еще в разработке')


@dp.message_handler(Text(equals='Информация'))
async def info(message: types.Message):
    await message.answer('Данный бот принимает карты ТОЛЬКО с сайта: https://www.cardkingdom.com')
    await message.answer('Для комфотной работы отправляйте запросы только после полученного ответа')


@dp.message_handler(Text(equals='Удалить карту'))
async def info(message: types.Message):
    await message.answer('Введите ссылку карты, которую хотите удалить')

    @dp.message_handler(content_types=["text"])
    async def minimum(message: types.Message):
        url = message.text.strip()
        result = delete_card(message.from_user.username, url)
        if result == 1:
            await message.answer('Карта успешно удалена')
        elif result == 404:
            await message.answer('Ссылка введена не верно')


def main():
    executor.start_polling(dp)


if __name__ == '__main__':
    main()

import io
import re

import pandas as pd
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from database.commands import telegram_users
from database.commands.location import select_location, add_location
from handlers.commands import cancel
from keyboards.reply import confirm_photo_load_kb, start_menu_kb, next_load_kb
from loader import dp, bot
from names import SEVERAL_HOTELS, CANCEL, PHOTOS, CONFIRM, NEXT


def extract_text(flag, text):
    pattern = r'\[{}](.*?)\[/{}\]'.format(flag, flag)
    match = re.findall(pattern, text, re.DOTALL)
    return match[0].strip() if match else None


class CSVFile(StatesGroup):
    waiting_for_csv = State()
    load_photos = State()
    loop_hotels_load_photos = State()


@dp.callback_query_handler(text=SEVERAL_HOTELS, state='*')
async def multiple_hotels_handler(callback_query: types.CallbackQuery):
    chat_id = callback_query.from_user.id
    if not await telegram_users.user_is_admin(chat_id):
        return

    await bot.send_message(
        chat_id,
        "Загрузите выгруженную информацию с Конструктора Яндекс Карт.\nCSV файл, в котором разделителем является символ \";\"."
    )
    await CSVFile.waiting_for_csv.set()


@dp.message_handler(content_types=['document'], state=CSVFile.waiting_for_csv)
async def process_csv_file(message: types.Message, state: FSMContext):
    chat_id = message.from_user.id
    csv_file = message.document
    if 'csv' in csv_file.mime_type:
        content = io.BytesIO()
        await message.document.download(content)
        content.seek(0)
        df = pd.read_csv(content, delimiter=';')
        locations = []
        for _, row in df.iterrows():
            template_text = row['Описание']
            try:
                title, desc, lat, long, short_desc, price, schedule, link, cat_filter, emodji = row.get('Подпись'), \
                                                                                                extract_text('DESC', template_text), \
                                                                                                row['Широта'], row['Долгота'], \
                                                                                                extract_text('SHORT_DESC', template_text), \
                                                                                                extract_text('PRICE', template_text), \
                                                                                                extract_text('SCHEDULE', template_text), \
                                                                                                extract_text('LINK', template_text), \
                                                                                                extract_text('FILTER', template_text), \
                                                                                                extract_text('EMODJI', template_text)

                if not await select_location(title=title, description=desc, latitude=lat, longitude=long):
                    loc = await add_location(row.get('Подпись'), extract_text('DESC', template_text),
                                                short_desc, price, schedule, lat, long, "", link, cat_filter, emodji)
                    locations.append(loc)
            except:
                pass
        async with state.proxy() as data:
            try:
                data['locations'] = locations
                pop = data['locations'].pop(0)
                id, title = pop
                data['current'] = id

                await message.answer(
                    f'<b>Загрузите фото для локации - <i>"{title}"</i></b>',
                    reply_markup=confirm_photo_load_kb
                )
                await CSVFile.load_photos.set()
            except Exception as ex:
                print(ex)
                await message.answer(f'<b>Не найдено новых объектов!</b>')
                await state.finish()
    else:
        await message.answer("Файл должен быть в формате CSV. Попробуйте ещё раз!")


@dp.message_handler(state=CSVFile.loop_hotels_load_photos)
async def loop_load_photos(message: types.Message, state: FSMContext):
    chat_id = message.from_user.id
    if message.text == NEXT:
        async with state.proxy() as data:
            if data.get('locations'):
                pop = data['locations'].pop(0)
                id, title = pop
                data['current'] = id
                await message.answer(
                    f'<b>Загрузите фото для локации - <i>"{title}"</i></b>',
                    reply_markup=confirm_photo_load_kb
                )
                await CSVFile.load_photos.set()
            else:
                await message.answer(
                    'Фотографии для всех локаций были загружены!')
                await state.finish()


@dp.message_handler(state=CSVFile.load_photos, content_types=types.ContentType.PHOTO)
async def load_photos(message: types.Message, state: FSMContext):
    if CANCEL == message.text:
        return await cancel(message)

    photo = message.photo[-1]
    async with state.proxy() as data:
        if PHOTOS in data:
            data[PHOTOS].append(photo)
        else:
            data[PHOTOS] = [photo]

    await CSVFile.load_photos.set()


@dp.message_handler(state=CSVFile.load_photos, text_contains=CONFIRM)
async def confirm_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        hotel_id = data['current']
        for i, photo in enumerate(data[PHOTOS]):
            await photo.download(destination_file=f'storage/photos/hotel_{hotel_id}/photo_{i}.jpg')

        await message.answer(
            f'<b>Изображения были успешно сохранены!</b>',
            reply_markup=next_load_kb
        )
        data.pop(PHOTOS)
    await CSVFile.loop_hotels_load_photos.set()


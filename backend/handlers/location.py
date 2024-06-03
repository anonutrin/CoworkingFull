import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hbold

import names
from config.settings import settings
from database.commands.location_visit_stats import select_or_create_location_visit_stat, update_location_visit_stat
from database.commands.telegram_users import update_user_location
from handlers.admin.catalog import send_location_info
from keyboards.inline import generate_location_kb, generate_menu_kb
from keyboards.reply import start_menu_kb, get_city_kb
from loader import dp
from names import CHANGE_LOCATION
from states.location import StateLocation


@dp.message_handler(text=[CHANGE_LOCATION], state='*')
async def change_location(message: types.Message):
    await message.answer(f'Выберите свой город: ', reply_markup=get_city_kb())
    await StateLocation.city.set()


@dp.callback_query_handler(text_contains="change_location")
async def change_location_handler(callback: types.CallbackQuery):
    await StateLocation.city.set()
    await callback.message.edit_text(
        'Выберите свой город: ',
        reply_markup=await generate_location_kb(list(settings.CITIES.keys()))
    )


@dp.callback_query_handler(state=StateLocation.city)
async def chose_location_handler(callback: types.CallbackQuery, state: FSMContext):
    try:
        location = callback.data
        locations = list(settings.CITIES.keys())
        if location not in locations:
            return await state.finish()

        await update_user_location(callback.from_user.id, location)
        await callback.message.edit_text('Вы успешно изменили свою геолокацию!',
                                         reply_markup=await generate_menu_kb(callback.from_user.id))
    except Exception as ex:
        logging.error(f'chose_location_handler err: {ex}')


@dp.message_handler(state=StateLocation.city)
async def get_city(message: types.Message, state: FSMContext):
    chat_id = message.from_user.id
    city = message.text
    try:
        await update_user_location(chat_id, city)
        await message.answer(hbold('Вы успешно изменили свою геолокацию!'))
        await state.finish()
    except:
        await message.answer(hbold('Выберите город из данного списка!'), reply_markup=get_city_kb())


@dp.callback_query_handler(text_contains=names.__SH)
async def show_location_handler(callback: types.CallbackQuery):
    try:
        chat_id = callback.from_user.id
        location_id, flag = callback.data.split(settings.SEP)
        await callback.message.delete()
        await send_location_info(chat_id, int(location_id))
        location_visit_stat = await select_or_create_location_visit_stat(chat_id, int(location_id))
        await update_location_visit_stat(location_visit_stat)

    except Exception as ex:
        await callback.message.answer('Произошла ошибка при получении локации :(')
        logging.error(f'show_location_handler error: {ex}')

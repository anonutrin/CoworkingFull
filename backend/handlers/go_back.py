from aiogram import types

from config.settings import settings
from keyboards.inline import catalog_actions_kb
from names import __BACK, CATALOG_MANAGE

from loader import dp


@dp.callback_query_handler(text_contains=__BACK)
async def go_back(callback: types.CallbackQuery):
    to = callback.data.split(settings.SEP)[0]

    if to in [CATALOG_MANAGE]:
        await callback.message.edit_text('Выберите действие:', reply_markup=await catalog_actions_kb())
    else:
        pass

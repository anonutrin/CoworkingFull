from aiogram import types
from aiogram.dispatcher.filters import Command

from database.commands.bot_activation_stats import export_bot_activation_stats_to_excel
from database.commands.location_visit_stats import export_location_visit_stats_to_excel
from database.commands.telegram_users import user_is_admin
from loader import dp
from utils.logger import logger


@dp.message_handler(Command("export_visit_stats"))
async def export_location_visit_stats_to_excel_handler(message: types.Message):
    if not await user_is_admin(message.from_user.id):
        return
    try:
        file_path = await export_location_visit_stats_to_excel()
        await message.answer_document(types.InputFile(file_path))
    except Exception as ex:
        logger.error(ex)


@dp.message_handler(Command("export_bot_activation_stats"))
async def export_bot_activation_stats_to_excel_handler(message: types.Message):
    if not await user_is_admin(message.from_user.id):
        return
    try:
        file_path = await export_bot_activation_stats_to_excel()
        await message.answer_document(types.InputFile(file_path))
    except Exception as ex:
        logger.error(ex)


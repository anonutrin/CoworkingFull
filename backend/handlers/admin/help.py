from aiogram import types
from aiogram.dispatcher.filters import Command
from database.commands.telegram_users import user_is_admin
from loader import dp
from utils.logger import logger


@dp.message_handler(Command("help"))
async def get_help_info_handler(message: types.Message):
    if not await user_is_admin(message.from_user.id):
        return
    try:
        await message.answer('<b>Доступные комманды:</b>\n\n'
                             '<code>/export_visit_stats</code> - Выгрузка статистики по локациям\n'
                             '<code>/export_bot_activation_stats</code> - Выгрузка статистики активаций бота\n'
                             '<code>/export_locations</code> - Экспорт локаций из GoogleSheet')
    except Exception as ex:
        logger.error(f'An error occurred while handle help command: {ex}')

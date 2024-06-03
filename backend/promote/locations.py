import asyncio
from utils.logger import logger

from aiogram.types import ParseMode

from database.commands import telegram_users
from keyboards.prmoted.location_kb import keyboard_for_promoted_location
from loader import bot


async def send_promoted_locations(chat_id, promoted_location_id, promoted_text):
    await bot.send_message(
        chat_id, promoted_text,
        reply_markup=await keyboard_for_promoted_location(promoted_location_id),
        parse_mode=ParseMode.MARKDOWN
    )


async def newsletter_for_all_users_promoted_location(promoted_location_id, promoted_text):
    users = await telegram_users.select_users()
    for user in users:
        try:
            await send_promoted_locations(user.user_id, promoted_location_id, promoted_text)
        except Exception as ex:
            logger.error(f'Не удалось отправить продвигаемую локацию: {locals()}: {ex}')

        await asyncio.sleep(0.1)

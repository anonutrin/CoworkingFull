from database.commands.location_visit_stats import select_or_create_location_visit_stat, update_location_visit_stat
from handlers.admin.catalog import send_location_info
from loader import dp
from utils.logger import logger

HOTEL_PHOTOS_DIR = "storage/photos"


@dp.message_handler(content_types='web_app_data')
async def show_location(wa):
    try:
        chat_id = wa.from_user.id
        location_id = wa.web_app_data.data
        location_id = location_id.replace("'", '')
        location_visit_stat = await select_or_create_location_visit_stat(chat_id, location_id)
        await update_location_visit_stat(location_visit_stat)
        await send_location_info(chat_id, int(location_id))
    except Exception as e:
        logger.error(f'An error occurred while WebApp show location: {e}')


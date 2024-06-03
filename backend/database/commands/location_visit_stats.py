import logging
from typing import Optional

from admin_dashboard.master_locations.models import LocationVisitStats
from config.settings import settings
from database.commands import telegram_users
from database.commands import location


async def select_or_create_location_visit_stat(user_id, location_id):
    """ Get location stat query.
        Return None if error """
    try:
        user = await telegram_users.select_user(user_id)
        location_item = await location.select_location_by_id(location_id)
        location_item.views_count += 1
        location_item.save()
        location_statistics, created = LocationVisitStats.objects.get_or_create(user=user, location=location_item)
        return location_statistics
    except Exception as ex:
        logging.error(f'[err] select_location_visit_stat ({locals()}) - {ex}')
        return None


async def update_location_visit_stat(location_visit_stats: Optional[LocationVisitStats]):
    if location_visit_stats is None:
        return False
    try:
        location_visit_stats.visit_count += 1
        location_visit_stats.save()
        return True
    except Exception as ex:
        logging.error(f'[err] update_location_visit_stat ({locals()}) - {ex}')
        return False


async def export_location_visit_stats_to_excel():
    try:
        location_visit_stats_df = LocationVisitStats.to_pandas()

        file_name = "location_visit_stats.xlsx"
        full_path = settings.TEMP_FOLDER_PATH + file_name
        location_visit_stats_df.to_excel(full_path, sheet_name='Статистика локаций', index=False)
        return full_path
    except Exception as ex:
        print(f'[err] export_location_visit_stats_to_excel - {ex}')
        # logging.error()

    # with open(file_name, "rb") as excel_file:
    #     await message.answer_document(InputFile(excel_file, file_name))

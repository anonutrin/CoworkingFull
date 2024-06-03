from datetime import date

from admin_dashboard.master_locations.models import BotActivationStat
from config.settings import settings
from utils.logger import logger


async def increment_activation_count():
    try:
        today = date.today()

        try:
            stats = BotActivationStat.objects.get(date_activation=today)
            stats.activation_count += 1
            stats.save()
        except BotActivationStat.DoesNotExist:
            BotActivationStat.objects.create(date_activation=today, activation_count=1)
    except Exception as ex:
        logger.error(ex)


async def export_bot_activation_stats_to_excel():
    try:
        location_visit_stats_df = BotActivationStat.to_pandas()

        file_name = "bot_activation_stats.xlsx"
        full_path = settings.TEMP_FOLDER_PATH / file_name
        location_visit_stats_df.to_excel(full_path, sheet_name='Статистика активаций бота', index=False)
        return full_path
    except Exception as ex:
        logger.error(ex)


from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config.settings import settings

from database.services.export_gsheet_table_service import ExportGSheetTableService
from google_services.gdrive.service import GDriveService
from google_services.geomap.yandex_geocoder import GeoLocator


bot = Bot(settings.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
bot.default_parse_mode = types.ParseMode.HTML
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

gdrive_service = GDriveService(settings.GOOGLE_API_CREDENTIALS_PATH)


export_gsheet_service = ExportGSheetTableService(
    link_to_worksheet=settings.GOOGLE_WORKSHEET_LINK,
    credentials_path=settings.GOOGLE_SHEET_API_CREDENTIALS_PATH
)
export_auto_service = ExportGSheetTableService(
    link_to_worksheet=settings.GOOGLE_AUTO_WORKSHEET_LINK,
    credentials_path=settings.GOOGLE_SHEET_API_CREDENTIALS_PATH
)

geo_locator = GeoLocator(settings.YANDEX_API_KEY)

import re
from typing import Optional, List

from aiogram import types
from aiogram.dispatcher.filters import Command

from config.settings import settings
from database.commands.location import update_or_create_location
from database.commands.telegram_users import user_is_admin
from database.validators.location_validator import LocationValidator
from loader import dp, export_gsheet_service, gdrive_service, geo_locator
from utils.file_manager import create_folder_if_not_exist
from utils.logger import logger
from contextlib import suppress


def extract_id_from_google_drive_link(link):
    match = re.search(r'/folders/([^/?]+)', link)
    return match.group(1) if match else None


@dp.message_handler(Command("export_locations"))
async def export_locations_from_gsheet_handler(message: types.Message):
    if not await user_is_admin(message.from_user.id):
        return
    try:
        await message.answer('Запрос на экспорт таблицы из GoogleSheet подан. Ожидайте завершения экспорта...')
        locations: Optional[List[LocationValidator]] = await export_gsheet_service.export_table(validator=LocationValidator)
        if not locations:
            raise Exception('Locations not found')

        logger.info('Starting export location from GSheet')
        locations_size = len(locations)

        gdrive_service.authenticate()
        await geo_locator.set_aiohttp_session()

        for idx, location in enumerate(locations):
            folder_path = f'{settings.IMAGES_FOLDER_PATH}/location_{location.location_id}'
            logger.info(f'Location {idx + 1} / {locations_size}:\n{location.model_dump()}\n'
                        f'Folder path: {folder_path}')

            if not await create_folder_if_not_exist(folder_path):
                raise Exception()

            if location.latitude is None or location.longitude is None \
                    or location.latitude == '' or location.longitude == '':
                if location.full_address:
                    coordinates = await geo_locator.get_coordinates(location.full_address)

                    if coordinates:
                        location.latitude = coordinates[1]
                        location.longitude = coordinates[0]
                else:
                    location.latitude = None
                    location.longitude = None
            else:
                with suppress(ValueError):
                    location.latitude = float(location.latitude)
                    location.longitude = float(location.longitude)

            if location.images_link != '' and location.images_link:
                gdrive_service.download_images_from_folder(extract_id_from_google_drive_link(location.images_link), folder_path)

            updated_location, is_created = await update_or_create_location(
                **location.model_dump(exclude={'images_link'}),
            )

            if is_created:
                logger.debug(f'Location #{idx + 1} has been created in Location model!')
            else:
                logger.debug(f'Location #{idx + 1} has been updated in Location model!')

            logger.info(f'Location #{idx+1} successfully exported!')

        await geo_locator.close_aiohttp_session()
        await message.answer('Таблица успешно экспортирована!')
    except Exception as ex:
        await geo_locator.close_aiohttp_session()
        logger.error(f'An error occurred while exporting locations from gsheet: {ex}')
        await message.answer('Произошла ошибка при экспорте локаций из гугл таблицы :(')


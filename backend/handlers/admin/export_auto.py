import re
from typing import Optional, List

from aiogram import types
from aiogram.dispatcher.filters import Command

from config.settings import settings
from database.commands.auto import update_or_create_auto
from database.commands.telegram_users import user_is_admin
from database.validators.auto_validator import AutoValidator
from loader import dp, gdrive_service, export_auto_service
from utils.file_manager import create_folder_if_not_exist
from utils.logger import logger


def extract_id_from_google_drive_link(link):
    match = re.search(r'/folders/([^/?]+)', link)
    return match.group(1) if match else None


@dp.message_handler(Command("export_auto"))
async def export_autos_from_gsheet_handler(message: types.Message):
    if not await user_is_admin(message.from_user.id):
        return
    try:
        await message.answer('Запрос на экспорт таблицы из GoogleSheet подан. Ожидайте завершения экспорта...')
        autos: Optional[List[AutoValidator]] = await export_auto_service.export_table(validator=AutoValidator)
        if not autos:
            raise Exception('Autos not found')

        logger.info('Starting export autos from GSheet')
        auto_size = len(autos)

        gdrive_service.authenticate()

        for idx, auto in enumerate(autos):
            folder_path = f'{settings.AUTO_IMAGES_FOLDER_PATH}/auto_{auto.number}'
            logger.info(f'Location {idx + 1} / {auto_size}:\n{auto.model_dump()}\n'
                        f'Folder path: {folder_path}')

            if not await create_folder_if_not_exist(folder_path):
                raise Exception()

            if auto.images_link != '' and auto.images_link:
                gdrive_service.download_images_from_folder(extract_id_from_google_drive_link(auto.images_link), folder_path)

            updated_auto, is_created = await update_or_create_auto(
                **auto.model_dump(exclude={'images_link'})
            )

            if is_created:
                logger.debug(f'Auto #{idx + 1} has been created in Auto model!')
            else:
                logger.debug(f'Auto #{idx + 1} has been updated in Auto model!')

            logger.info(f'Auto #{idx+1} successfully exported!')

        await message.answer('Таблица успешно экспортирована!')
    except Exception as ex:
        logger.error(f'An error occurred while exporting autos from gsheet: {ex}')
        await message.answer('Произошла ошибка при экспорте авто из гугл таблицы :(')


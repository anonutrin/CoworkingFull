import os

from utils.logger import logger


async def remove_files_in_folder(folder_path):
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            logger.error(f"Error deleting file '{file_path}': {str(e)}")

    logger.debug(f'All files removed from {folder_path}')


async def create_folder_if_not_exist(folder_path):
    try:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            logger.debug(f"Folder '{folder_path}' has been created.")
        else:
            logger.debug(f"Folder '{folder_path}' exist.")
            await remove_files_in_folder(folder_path)
        return True
    except Exception as ex:
        logger.error(f'An error occurred while create folder if not exist ({folder_path}): {ex}')
        return False

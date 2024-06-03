import os

from aiogram.types import InputFile, InputMediaPhoto

from admin_dashboard.master_locations.models import Location

LOCATION_IMAGES_BASE_PATH = 'storage/images/location_'


async def return_media_by_location(location: Location):
    location_id = location.id
    dirname = f'{LOCATION_IMAGES_BASE_PATH}{location_id}'
    allowed_extensions = ('.jpg', '.jpeg', '.png')
    media = []
    try:
        files = os.listdir(dirname)
        files = [file for file in files if file.lower().endswith(allowed_extensions)]
        for file in files:
            if len(files) == 1:
                media.append(open(f'{dirname}/{file}', 'rb'))
            else:
                photo = InputFile(f'{dirname}/{file}')
                media.append(InputMediaPhoto(photo, caption=f"{location.title}"))

        return media
    except FileNotFoundError:
        print(f'{dirname} was not found!')
        return media

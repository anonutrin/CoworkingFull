from config.settings import settings
from loader import bot


async def get_user_avatar(user_id: int):
    try:
        profile_photos = await bot.get_user_profile_photos(user_id)
        if profile_photos.photos:
            photo = profile_photos.photos[0][0]  # Get the latest photo
            file_id = photo.file_id
            file = await bot.get_file(file_id)
            file_path = file.file_path

            photo_url = f"https://api.telegram.org/file/bot{settings.BOT_TOKEN}/{file_path}"
            return photo_url
        else:
            return None
    except Exception as ex:
        return None

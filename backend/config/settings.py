from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    # bot
    BOT_TOKEN: str
    YANDEX_API_KEY: str
    CHANNEL_LINK: str
    CHANNEL_ID: str
    GOOGLE_WORKSHEET_LINK: str
    GOOGLE_AUTO_WORKSHEET_LINK: str
    IMAGES_FOLDER_PATH: Path | str = BASE_DIR / 'storage' / 'images'
    AUTO_IMAGES_FOLDER_PATH: Path | str = BASE_DIR / 'storage' / 'images' / 'auto'
    LOGGER_PATH: Path | str = BASE_DIR / 'storage' / 'logs' / 'telegram_bot.log'
    GOOGLE_API_CREDENTIALS_PATH: Path | str = BASE_DIR / 'config' / 'google_credentials.json'
    GOOGLE_SHEET_API_CREDENTIALS_PATH: Path | str = BASE_DIR / 'config' / 'gsheet_cred.json'
    TEMP_FOLDER_PATH: Path | str = BASE_DIR / 'storage' / 'temp'
    WEB_APP_SITE: str = 'https://212.193.50.28:8026'
    CITIES: dict = {
        'Москва': [55.76, 37.64],
        'Санкт-Петербург': [59.93, 30.33],
        'Новосибирск': [55.00, 82.93]
    }
    SEP: str = '|'
    SERVER_HOST: str = '212.193.50.28'
    SERVER_PORT: int = 8099

    class Config:
        env_file = BASE_DIR / '.env'


settings = Settings()

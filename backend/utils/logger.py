from pathlib import Path

from loguru import logger

from config.settings import settings

BASE_DIR = Path(__file__).parent.parent


logger.add(settings.LOGGER_PATH, rotation="500 MB")

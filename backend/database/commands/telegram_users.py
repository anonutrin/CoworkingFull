import logging

from admin_dashboard.master_locations.models import TelegramUsers
from utils.logger import logger


async def select_user(user_id, **kwargs):
    """ Get user query.
    Return None if error """
    try:
        return TelegramUsers.objects.filter(user_id=user_id, **kwargs).first()
    except Exception as ex:
        logger.error(ex)
        return None


async def select_users(**kwargs):
    """ Get user query.
    Return empty list [] if error """
    try:
        return TelegramUsers.objects.filter(**kwargs).all()
    except Exception as ex:
        logger.error(ex)
        return []


async def update_user_location(chat_id, city):
    try:
        user = await select_user(chat_id)
        user.chose_location = city
        user.save()
    except Exception as ex:
        logger.error(ex)


async def add_user(user_id, username):
    user_id = user_id
    telegram_user, created = TelegramUsers.objects.get_or_create(
        user_id=user_id,
        defaults={
            'username': username,
        },

    )
    logging.log(logging.INFO, f'{telegram_user} | Created: {created}')


async def increase_bot_activation_count(chat_id):
    try:
        user = await select_user(chat_id)
        user.bot_activation_count += 1
        user.save()
    except Exception as ex:
        logger.error(ex)


async def user_is_admin(chat_id):
    try:
        user = await select_user(chat_id)
        if user:
            if user.is_admin:
                return True

        return False
    except Exception as ex:
        logger.error(ex)
        return False

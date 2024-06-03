import logging
from typing import List, Optional

from django.db import IntegrityError

from admin_dashboard.master_locations.app_models import TelegramUsers


class UserRepository:
    model: TelegramUsers = TelegramUsers

    def __init__(self):
        ...

    async def create_user(self, user_id, username) -> Optional[TelegramUsers]:
        try:
            telegram_user, created = self.model.objects.get_or_create(
                user_id=user_id,
                defaults={
                    'username': username,
                },

            )
            logging.info(f'{telegram_user} | Created: {created}')
            return telegram_user

        except IntegrityError as ie:
            logging.error(f'An error occurred while creating the user: {ie}')
            return None

    async def is_admin(self, chat_id) -> bool:
        try:
            user = await self.get_user_by_id(chat_id)
            if user:
                if user.is_admin:
                    return True

            return False
        except Exception as ex:
            logging.error(f'An error occurred while checking user is admin: {str(ex)}')
            return False

    async def get_user_by_id(self, user_id, **kwargs) -> Optional[TelegramUsers]:
        """ Get user query.
        Return None if error """
        try:
            return self.model.objects.filter(user_id=user_id, **kwargs).first()
        except Exception as ex:
            logging.error(f'An error occurred while get user by id: {user_id}. {ex}')
            return None

    async def get_all_users(self, **kwargs) -> Optional[List[TelegramUsers]]:
        """ Get user query.
        Return empty list [] if error """
        try:
            return self.model.objects.filter(**kwargs).all()
        except Exception as ex:
            logging.error(f'[err] select_users ({locals()}) - {ex}')
            return []

    async def increase_bot_activation_count(self, chat_id):
        try:
            user = await self.get_user_by_id(chat_id)
            user.bot_activation_count += 1
            user.save()
        except Exception as ex:
            logging.error(f'An error occurred while increase bot activation: {ex}')

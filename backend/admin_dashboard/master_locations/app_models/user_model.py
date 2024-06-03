from django.db import models
from ._constants import ConstantsTelegramUser, SupportedLocationChoice


class TelegramUsers(models.Model):
    user_id = models.IntegerField(verbose_name=ConstantsTelegramUser.user_id, unique=True)
    username = models.CharField(verbose_name=ConstantsTelegramUser.username, max_length=255, null=True, blank=True)

    is_admin = models.BooleanField(
        verbose_name=ConstantsTelegramUser.is_admin,
        default=False,
    )
    chose_location = models.CharField(
        verbose_name=ConstantsTelegramUser.chose_location,
        default=SupportedLocationChoice.moscow,
        max_length=SupportedLocationChoice.get_choice_max_length(),
        choices=SupportedLocationChoice.get_choices()
    )
    bot_activation_count = models.IntegerField(verbose_name=ConstantsTelegramUser.bot_activation_count, default=0)
    created_at = models.DateTimeField(
        verbose_name=ConstantsTelegramUser.created_at,
        auto_now_add=True,
        null=True
    )
    updated_at = models.DateTimeField(
        verbose_name=ConstantsTelegramUser.updated_at,
        auto_now=True,
        null=True
    )

    def __str__(self):
        return f'{self.username} ({self.user_id})'

    class Meta(ConstantsTelegramUser.Meta):
        ...


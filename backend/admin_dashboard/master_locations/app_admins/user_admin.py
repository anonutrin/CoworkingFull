from django.contrib import admin

from .base_admin import AutoConfigAdmin
from ..forms import TelegramUserForm
from ..models import TelegramUsers


@admin.register(TelegramUsers)
class UsersAdmin(AutoConfigAdmin):
    form = TelegramUserForm


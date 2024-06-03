from django.contrib import admin

from .base_admin import AutoConfigAdmin
from ..forms import BotActivationStatForm
from ..models import BotActivationStat


@admin.register(BotActivationStat)
class BotActivationStatAdmin(AutoConfigAdmin):
    form = BotActivationStatForm


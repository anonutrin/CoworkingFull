from django.contrib import admin

from .base_admin import AutoConfigAdmin
from ..forms import AutoForm
from ..models import Auto


@admin.register(Auto)
class AutoAdmin(AutoConfigAdmin):
    form = AutoForm

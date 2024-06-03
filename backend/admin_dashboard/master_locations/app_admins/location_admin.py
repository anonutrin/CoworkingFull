from django.contrib import admin

from .base_admin import AutoConfigAdmin
from ..forms import LocationForm
from ..models import Location


@admin.register(Location)
class LocationAdmin(AutoConfigAdmin):
    form = LocationForm


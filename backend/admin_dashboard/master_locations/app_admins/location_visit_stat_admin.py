from django.contrib import admin

from .base_admin import AutoConfigAdmin
from ..forms import LocationVisitStatForm
from ..models import LocationVisitStats


@admin.register(LocationVisitStats)
class LocationVisitStatAdmin(AutoConfigAdmin):
    form = LocationVisitStatForm


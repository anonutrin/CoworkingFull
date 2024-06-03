import os
import sys

from django.apps import AppConfig
sys.path.append(os.getcwd())
from django_configure import get_django_name


class MasterLocationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = get_django_name()

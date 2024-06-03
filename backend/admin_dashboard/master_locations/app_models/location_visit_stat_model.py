from django.db import models
from django_pandas.managers import DataFrameManager
import pandas as pd

from .user_model import TelegramUsers
from .location_model import Location
from ._constants import ConstantsLocationVisitStats as CLVS


class LocationVisitStats(models.Model):
    user = models.ForeignKey(TelegramUsers, verbose_name=CLVS.user, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, verbose_name=CLVS.location, on_delete=models.CASCADE)
    visit_count = models.IntegerField(verbose_name=CLVS.visit_count, default=0)

    created_at = models.DateTimeField(verbose_name=CLVS.created_at, auto_now_add=True, null=True)
    updated_at = models.DateTimeField(verbose_name=CLVS.updated_at, auto_now=True, null=True)
    objects = DataFrameManager()

    class Meta(CLVS.Meta):
        ...

    @classmethod
    def to_pandas(cls):
        dataframe = pd.DataFrame.from_records(
            cls.objects.all().values('user__user_id', 'user__username', 'location__id', 'location__title', 'visit_count')
        )
        dataframe = dataframe.rename(columns={
            'user__user_id': 'ID Пользователя',
            'user__username': 'Username',
            'location__id': 'ID локации',
            'location__title': 'Название локации',
            'visit_count': 'Кол-во переходов'
        })
        return dataframe


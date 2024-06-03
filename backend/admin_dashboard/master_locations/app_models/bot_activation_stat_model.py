from django.db import models
import pandas as pd
from django_pandas.managers import DataFrameManager

from ._constants import ConstantsBotActivationStat as CBAS


class BotActivationStat(models.Model):
    date_activation = models.DateField(verbose_name=CBAS.date_activation)
    activation_count = models.IntegerField(verbose_name=CBAS.activation_count, default=0)
    objects = DataFrameManager()

    class Meta(CBAS.Meta):
        ...

    @classmethod
    def to_pandas(cls):
        dataframe = pd.DataFrame.from_records(
            cls.objects.all().values('date_activation', 'activation_count')
        )
        dataframe = dataframe.rename(columns={
            'date_activation': 'Дата активации',
            'activation_count': 'Кол-во активаций',
        })
        return dataframe

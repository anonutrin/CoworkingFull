from django.db import models
from ._constants import ConstantsAuto


class Auto(models.Model):
    id = models.AutoField(primary_key=True, verbose_name=ConstantsAuto.id)
    brand = models.CharField(max_length=256, verbose_name=ConstantsAuto.brand)
    model = models.CharField(max_length=256, verbose_name=ConstantsAuto.model)
    equipment = models.TextField(verbose_name=ConstantsAuto.equipment)
    year_of_issue = models.IntegerField(verbose_name=ConstantsAuto.year_of_issue, blank=True, null=True)
    class_type = models.CharField(max_length=256, verbose_name=ConstantsAuto.class_type, blank=True, null=True)
    color = models.CharField(max_length=256, verbose_name=ConstantsAuto.color, blank=True, null=True)
    body = models.CharField(max_length=256, verbose_name=ConstantsAuto.body, blank=True, null=True)
    drive_unit = models.CharField(max_length=256, verbose_name=ConstantsAuto.drive_unit, blank=True, null=True)
    fuel_type = models.CharField(max_length=256, verbose_name=ConstantsAuto.fuel_type, blank=True, null=True)
    transmission = models.CharField(max_length=256, verbose_name=ConstantsAuto.transmission, blank=True, null=True)
    power = models.IntegerField(verbose_name=ConstantsAuto.power, blank=True, null=True)
    volume_engine = models.DecimalField(verbose_name=ConstantsAuto.volume_engine, blank=True, null=True,
                                        decimal_places=4, max_digits=8)
    fuel_volume = models.IntegerField(verbose_name=ConstantsAuto.fuel_volume, blank=True, null=True)
    acceleration_to100 = models.DecimalField(verbose_name=ConstantsAuto.acceleration_to100, blank=True, null=True,
                                             decimal_places=4, max_digits=8)
    seats_number = models.IntegerField(verbose_name=ConstantsAuto.seats_number, blank=True, null=True)
    city = models.CharField(max_length=256, verbose_name=ConstantsAuto.city, blank=True, null=True)
    rent_cost_per_day = models.CharField(max_length=256, verbose_name=ConstantsAuto.rent_cost_per_day, blank=True,
                                         null=True)
    rent_cost_per_month = models.CharField(max_length=256, verbose_name=ConstantsAuto.rent_cost_per_month, blank=True,
                                           null=True)
    description: str = models.TextField(verbose_name=ConstantsAuto.description, blank=True, null=True)
    links: str = models.TextField(verbose_name=ConstantsAuto.links, blank=True, null=True)

    def __str__(self):
        return f'Auto#{self.id} ({self.brand} {self.model})'

    class Meta(ConstantsAuto.Meta):
        ...

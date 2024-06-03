from django.db import models
from ._constants import ConstantsLocation, SupportedCategoriesChoice


class Location(models.Model):
    id = models.AutoField(primary_key=True, verbose_name=ConstantsLocation.id)
    title = models.CharField(max_length=256, verbose_name=ConstantsLocation.title)
    description = models.CharField(max_length=720, verbose_name=ConstantsLocation.description)
    short_description = models.CharField(max_length=256, verbose_name=ConstantsLocation.short_description)
    price = models.CharField(max_length=25, verbose_name=ConstantsLocation.price)
    price_number = models.FloatField(max_length=25, verbose_name=ConstantsLocation.price_number, default=0)
    contact_link = models.CharField(
        max_length=1024,
        verbose_name=ConstantsLocation.contact_link,
        default='', blank=True, null=True
    )
    emodji = models.CharField(max_length=10, verbose_name=ConstantsLocation.emodji, blank=True, null=True)
    work_schedule = models.CharField(max_length=25, verbose_name=ConstantsLocation.work_schedule, null=True, blank=True)
    latitude = models.FloatField(verbose_name=ConstantsLocation.latitude, blank=True, null=True)
    longitude = models.FloatField(verbose_name=ConstantsLocation.longitude, blank=True, null=True)
    full_address = models.CharField(max_length=128, verbose_name=ConstantsLocation.full_address, blank=True, null=True)
    category = models.CharField(
        max_length=SupportedCategoriesChoice.get_choice_max_length(),
        verbose_name=ConstantsLocation.category, choices=SupportedCategoriesChoice.get_choices(),
        default=SupportedCategoriesChoice.all
    )
    views_count = models.IntegerField(verbose_name=ConstantsLocation.views_count, default=0)

    def __str__(self):
        return f'Location#{self.id} ({self.title})'

    class Meta(ConstantsLocation.Meta):
        ...
            

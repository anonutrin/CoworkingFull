# Generated by Django 4.1.3 on 2024-05-14 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master_locations', '0023_alter_auto_equipment_alter_auto_rent_cost_per_day_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='price_number',
            field=models.CharField(default=0, max_length=25, verbose_name='Цена (Число)'),
        ),
    ]
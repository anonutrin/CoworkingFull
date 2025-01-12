# Generated by Django 4.1.3 on 2024-03-19 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master_locations', '0022_auto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auto',
            name='equipment',
            field=models.TextField(verbose_name='Комплектация'),
        ),
        migrations.AlterField(
            model_name='auto',
            name='rent_cost_per_day',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Стоимость аренды 1-2 суток'),
        ),
        migrations.AlterField(
            model_name='auto',
            name='rent_cost_per_month',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Стоимость аренды 30+ дней'),
        ),
    ]

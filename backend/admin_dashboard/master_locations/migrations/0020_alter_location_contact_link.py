# Generated by Django 4.1.3 on 2023-11-28 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master_locations', '0019_alter_location_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='contact_link',
            field=models.CharField(blank=True, default='', max_length=1024, null=True, verbose_name='Контактная ссылка'),
        ),
    ]

# Generated by Django 4.1.3 on 2023-08-21 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master_locations', '0010_photo_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='contact_link',
            field=models.CharField(blank=True, default='', max_length=128, null=True, verbose_name='Контактная ссылка'),
        ),
    ]
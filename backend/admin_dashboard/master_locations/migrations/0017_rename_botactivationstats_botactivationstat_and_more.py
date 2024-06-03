# Generated by Django 4.1.3 on 2023-11-09 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master_locations', '0016_botactivationstats'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='BotActivationStats',
            new_name='BotActivationStat',
        ),
        migrations.AlterModelOptions(
            name='location',
            options={'verbose_name': 'Локация'},
        ),
        migrations.AlterField(
            model_name='location',
            name='category',
            field=models.CharField(choices=[('all', 'Все'), ('colorist', 'Колорист'), ('hairdresser', 'Парикмахер'), ('manicurist', 'Маникюр'), ('visagiste', 'Визажист')], default='Все', max_length=11, verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='location',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='location',
            name='longitude',
            field=models.FloatField(blank=True, null=True, verbose_name='Долгота'),
        ),
        migrations.AlterField(
            model_name='telegramusers',
            name='chose_location',
            field=models.CharField(choices=[('moscow', 'Москва'), ('novosibirsk', 'Новосибирск'), ('saint_petersburg', 'Санкт-Петербург')], default='Москва', max_length=16, verbose_name='Выбрана локация'),
        ),
        migrations.AlterField(
            model_name='telegramusers',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created at'),
        ),
        migrations.AlterField(
            model_name='telegramusers',
            name='is_admin',
            field=models.BooleanField(default=False, verbose_name='Admin'),
        ),
        migrations.AlterField(
            model_name='telegramusers',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Updated at'),
        ),
        migrations.AlterField(
            model_name='telegramusers',
            name='user_id',
            field=models.IntegerField(unique=True, verbose_name='User ID'),
        ),
        migrations.AlterField(
            model_name='telegramusers',
            name='username',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='@username'),
        ),
    ]

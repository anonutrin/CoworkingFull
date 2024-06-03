# Generated by Django 4.1.3 on 2023-08-20 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='id')),
                ('title', models.CharField(max_length=256, verbose_name='Название')),
                ('description', models.CharField(max_length=512, verbose_name='Описание')),
                ('short_description', models.CharField(max_length=128, verbose_name='Краткое описание (для карты)')),
                ('price', models.CharField(max_length=25, verbose_name='Цена')),
                ('work_schedule', models.CharField(blank=True, max_length=25, null=True, verbose_name='График работы')),
                ('latitude', models.FloatField(verbose_name='Долгота')),
                ('longitude', models.FloatField(verbose_name='Широта')),
                ('category', models.CharField(max_length=15, verbose_name='Категория')),
            ],
        ),
        migrations.CreateModel(
            name='TelegramUsers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(unique=True, verbose_name='user_id')),
                ('username', models.CharField(blank=True, max_length=255, null=True, verbose_name='username')),
                ('is_admin', models.BooleanField(default=False, null=True, verbose_name='Администратор')),
                ('chose_location', models.CharField(blank=True, max_length=255, null=True, verbose_name='Выбрана локация')),
                ('chose_sphere', models.CharField(blank=True, max_length=255, null=True, verbose_name='Выбрана сфера')),
                ('chose_price', models.IntegerField(blank=True, null=True, verbose_name='Выбрана цена')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Создано')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Обновлено')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
    ]

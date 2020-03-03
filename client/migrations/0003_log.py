# Generated by Django 3.0.3 on 2020-02-27 19:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0002_auto_20200205_1620'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('action', models.CharField(choices=[('1', 'Вход в систему'), ('2', 'Выход из системы'), ('3', 'Добавление документа'), ('4', 'Редактирование документа'), ('5', 'Удаление документа'), ('6', 'Запрос на скачивание документа'), ('7', 'Активация'), ('8', 'Деактивация'), ('9', 'Регистрация'), ('10', 'Вход в системы с помощью фото')], default=0, max_length=100, verbose_name='Действие')),
                ('photo', models.CharField(max_length=100, verbose_name='URL фото по которому входили')),
                ('id_client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='client.Client', verbose_name='Клиент')),
            ],
            options={
                'verbose_name': 'Лог пользователя',
                'verbose_name_plural': 'Логи пользователей',
                'ordering': ['-date_created'],
            },
        ),
    ]

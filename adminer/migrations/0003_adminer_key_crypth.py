# Generated by Django 3.0.3 on 2020-02-11 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminer', '0002_auto_20200205_1620'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminer',
            name='key_crypth',
            field=models.CharField(blank=True, max_length=100, verbose_name='Ключ шифрования'),
        ),
    ]

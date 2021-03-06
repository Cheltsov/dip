# Generated by Django 3.0.3 on 2020-02-09 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0003_auto_20200206_2354'),
    ]

    operations = [
        migrations.AddField(
            model_name='doc',
            name='active',
            field=models.BooleanField(blank=True, default=1, max_length=1, verbose_name='Активность'),
        ),
        migrations.AlterField(
            model_name='doc',
            name='crypth',
            field=models.CharField(blank=True, choices=[('0', 'Без шифрования'), ('1', 'Электронная подпись DSA'), ('2', 'Электронная подпись RSA'), ('3', 'Шифр AES'), ('4', 'Шифр TripleDES')], default=0, max_length=1, verbose_name='Метод шифрования'),
        ),
    ]

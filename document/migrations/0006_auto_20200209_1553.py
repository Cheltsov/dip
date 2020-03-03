# Generated by Django 3.0.3 on 2020-02-09 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0005_auto_20200209_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doc',
            name='crypth',
            field=models.CharField(choices=[('0', 'Без шифрования'), ('1', 'Электронная подпись DSA'), ('2', 'Электронная подпись RSA'), ('3', 'Шифр AES'), ('4', 'Шифр TripleDES')], default='0', max_length=1, verbose_name='Метод шифрования'),
        ),
    ]

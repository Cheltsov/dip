# Generated by Django 3.0.3 on 2020-02-20 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0014_auto_20200221_0044'),
    ]

    operations = [
        migrations.AddField(
            model_name='doc',
            name='run',
            field=models.BooleanField(default=1, max_length=1, verbose_name='Флаг первого шифрования'),
        ),
    ]

# Generated by Django 3.0.3 on 2020-02-27 19:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0003_log'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='id_client',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='client.Client', verbose_name='Клиент'),
        ),
    ]
from django.db import models
from client.models import Client
from .utilities import get_timestamp_path

# Create your models here.
class Doc(models.Model):
    CRYPTH_METHODS = (
        ("1", 'Шифр AES'),
        ("2", 'Шифр TripleDES'),
    )

    title = models.CharField(max_length=100, verbose_name="Название")
    file = models.FileField(blank=True, verbose_name="Файл", upload_to=get_timestamp_path)
    client = models.ForeignKey(Client, on_delete=models.PROTECT, verbose_name="Создатель")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    date_updated = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    crypth = models.CharField(max_length=1, choices=CRYPTH_METHODS, verbose_name="Метод шифрования", default=0)
    active = models.BooleanField(max_length=1, verbose_name="Активность", default=1)
    decrypth = models.BooleanField(max_length=1, verbose_name="Расшифровать", default=0)
    finish = models.BooleanField(max_length=1,  verbose_name="Закончил шифрование", default=1)
    run = models.BooleanField(max_length=1,  verbose_name="Флаг первого шифрования", default=1)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Документы'
        verbose_name = 'Документ'
        ordering = ['-date_created']

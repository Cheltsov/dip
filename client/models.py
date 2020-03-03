from django.db import models
from .utilities import get_timestamp_path

# Create your models here.
class Client(models.Model):
    fio = models.CharField(max_length=50, verbose_name="ФИО", blank=True)
    photo = models.ImageField(blank=True, upload_to=get_timestamp_path, verbose_name='Фото')
    email = models.EmailField(max_length=100, verbose_name="Email", blank=True)
    password = models.CharField(max_length=100, verbose_name="Пароль", blank=True)
    active = models.BooleanField(max_length=1, verbose_name="Активность", blank=True)
    status = models.BooleanField(max_length=1, verbose_name="Сложная авторизация", blank=True)

    def __str__(self):
        return self.fio

    def check_client(self):
        tmp = Client.objects.filter(email=self.email, password=self.password, active=1).values_list('id', flat=True)
        if tmp:
            return tmp[0]
        else:
            return False

    def get_client_id(id):
        tmp = Client.objects.get(pk=id)
        return tmp

    class Meta:
        ordering = ['fio']
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

class Log(models.Model):
    ACTIONS = (
        ("1", 'Вход в систему'),
        ("2", 'Выход из системы'),
        ("3", 'Добавление документа'),
        ("4", 'Редактирование документа'),
        ("5", 'Удаление документа'),
        ("6", 'Запрос на скачивание документа'),
        ("7", 'Активация'),
        ("8", 'Деактивация'),
        ("9", 'Регистрация'),
        ("10", 'Вход в систему с помощью фото'),
    )

    id_client = models.ForeignKey(Client, on_delete=models.PROTECT, verbose_name="Клиент")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    action = models.CharField(max_length=100, verbose_name='Действие', choices=ACTIONS, default=0)
    #photo = models.CharField(max_length=100, verbose_name="URL фото по которому входили", blank=True)
    photo = models.FileField(blank=True, verbose_name="URL фото по которому входили", upload_to='face/')

    class Meta:
        ordering = ['-date_created']
        verbose_name = 'Лог пользователя'
        verbose_name_plural = 'Логи пользователей'

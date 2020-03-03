from django.db import models

# Create your models here.
class Adminer(models.Model):
    email = models.EmailField(max_length=100, verbose_name="Email", blank=True)
    password = models.CharField(max_length=100, verbose_name="Пароль", blank=True)

    def __str__(self):
        return self.email

    def check_admin(self):
        tmp = Adminer.objects.filter(email=self.email, password=self.password)
        return tmp

    class Meta:
        ordering = ['email']
        verbose_name = 'Администратор'
        verbose_name_plural = 'Администраторы'

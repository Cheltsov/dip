from django.contrib import admin
from .models import Client
from .models import Log

# Register your models here.
admin.site.register(Client)
admin.site.register(Log)

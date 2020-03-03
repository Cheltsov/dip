from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "adminer"
urlpatterns = [
    path('^$', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('documents/', views.document, name='document'),
    path('document_add/', views.document_add, name='document_add'),
    path('document_edit/<int:id>', views.document_edit, name='document_edit'),
    path('document_del/<int:id>', views.document_del, name='document_del'),
    path('settings/', views.settings, name='settings'),
    path('client/', views.client, name='client'),
    path('client_add/', views.client_add, name='client_add'),
    path('client_edit/<int:id>', views.client_edit, name='client_edit'),
    path('client_del/<int:id>', views.client_del, name='client_del'),
    path('exit/', views.exit, name='exit'),
    path('log/', views.log, name='log'),
    path('log_del/<int:id>', views.log_del, name='log_del'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

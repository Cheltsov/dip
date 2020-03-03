from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "client"
urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('document/', views.document, name='document'),
    path('document/add/', views.document_add, name='document_add'),
    path('document/edit/<int:id>', views.document_edit, name='document_edit'),
    path('document/del/<int:id>', views.document_del, name='document_del'),
    path('check_face/', views.check_face, name='check_face'),
    path('exit/', views.exit, name='exit'),
    path('add_client/', views.add_client, name='add_client'),
    path('edit_client/<int:id>', views.edit_client, name='edit_client'),
    path('search/', views.search, name='search'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


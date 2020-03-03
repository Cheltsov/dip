from django.urls import path
from . import views

app_name = "document"
urlpatterns = [
    path('create/', views.create_doc, name='create_doc'),
    path('edit/<int:id>', views.edit_doc, name='edit_doc'),
    path('del/<int:id>', views.edit_doc, name='del'),
    path('update_dec/', views.get_decrypth, name='get_decrypth'),
    path('search/', views.search, name='search'),
    path('search_admin/', views.search_admin, name='search_admin'),
]

from django.urls import path
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('productos', views.productos, name='productos'),
    path('ofertas', views.ofertas, name='ofertas'),
    path('contacto', views.contacto, name='contacto'),
    path('administrator', views.administrator, name='administrator'),
    path('administrator/dashboard', views.dashboard, name='dashboard'), # <-- NUEVA RUTA
]

from django.urls import path
from App import views

urlpatterns = [
    path('Inicio/', views.inicio, name='inicio'),
    path('clientes/', views.clientes, name='clientes'),
    path('productos/', views.productos, name='productos'),
    path('compra/', views.compra, name='compra'),
    path('resenas/', views.resenas, name='resenas'),
]
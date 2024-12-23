
from django.urls import path
from App import views

urlpatterns = [
    path('Inicio/', views.inicio, name='inicio'),
    path('clientes/', views.clientes, name='clientes'),
    path('productos/', views.productos, name='productos'),
    path('compra/', views.compra, name='compra'),
    path('resenas/', views.resenas, name='resenas'),
]
forms_api = [
    path('formulario-cliente/', views.clientes_formulario, name='formulario_cliente'),
    path('formulario-resena/', views.formulario_resena, name='dejar_resena'),
    path('formulario-compra/', views.formulario_compra, name='formulario_compra'),
    path('formulario-prodsinstock/', views.formulario_producto_fuera_stock, name='formulario_prodsinstock'),
]

# Añadiendo las rutas de los formularios al URL
urlpatterns += forms_api
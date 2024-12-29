
from django.urls import path
from App import views

urlpatterns = [
    path('inicio/', views.inicio, name='inicio'),
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
    path('buscar-cliente/', views.buscar_cliente, name='buscar_cliente'),
    path('buscar-producto/', views.buscar_producto, name='buscar_producto'),
    path('actualizar-cliente/<str:cliente_dni>/', views.actualizar_cliente, name='actualizar_cliente'),
    path('actualizar-producto/<str:sku>/', views.ProductoUpdateView.as_view(), name='actualizar_producto'),
    path('eliminar-producto/<str:sku>/', views.eliminar_producto, name='eliminar_producto'),
    path('producto-vbc/', views.ProductoListView.as_view()),
    path('producto/<str:sku>/', views.ProductoDetailView.as_view(), name='producto_detail'),
    path('producto/actualizar/<str:sku>/', views.ProductoUpdateView.as_view(), name='producto_update'),
    path('producto/eliminar/<str:sku>/', views.ProductoDeleteView.as_view(), name='producto_delete'),
    path('bienvenido/', views.bienvenido, name='bienvenido'),
    path('about/', views.about, name='about'),

]
    

# Añadiendo las rutas de los formularios al URL
urlpatterns += forms_api
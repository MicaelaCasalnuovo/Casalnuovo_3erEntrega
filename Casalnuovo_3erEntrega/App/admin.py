from django.contrib import admin
from App.models import ModeloCliente
from App.models import ModeloProducto
from App.models import ModeloReseña
from App.models import ModeloCompra

# Register your models here.
admin.site.register(ModeloCliente)
admin.site.register(ModeloProducto)
admin.site.register(ModeloReseña)
admin.site.register(ModeloCompra)
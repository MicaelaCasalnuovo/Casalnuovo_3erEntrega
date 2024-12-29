from django.db import models

# Create your models here.
class ModeloCliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=20, unique=True)
    direccion = models.TextField()
    celular = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

# Modelo Producto
class ModeloProducto(models.Model):
    sku = models.CharField(max_length=50, unique=True)  
    descripcion = models.TextField()
    stock = models.PositiveIntegerField()  
    precio = models.DecimalField(max_digits=10, decimal_places=2) 

    def __str__(self):
        return self.descripcion
from django.contrib.auth.models import User
class ModeloCompra(models.Model):
    producto = models.ForeignKey('ModeloProducto', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    nro_compra = models.CharField(max_length=20, unique=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # Cambiado a null=True temporalmente

    def __str__(self):
        return f"Compra {self.nro_compra} - {self.producto.descripcion} - {self.usuario.username if self.usuario else 'N/A'}"

    def __str__(self):
        return f"Compra {self.nro_compra} - {self.producto.descripcion} - {self.usuario.username}"

# Modelo Reseña
class ModeloReseña(models.Model):
    cliente = models.ForeignKey(ModeloCliente, on_delete=models.CASCADE)
    producto = models.ForeignKey(ModeloProducto, on_delete=models.CASCADE)
    comentario = models.TextField()

    def __str__(self):
        return f'Reseña de {self.cliente} para {self.producto}'

class SolicitudProductoFueraStock(models.Model):
    producto = models.CharField(max_length=255)  # Nombre del producto solicitado
    descripcion = models.TextField()  # Descripción opcional sobre el por qué lo buscan
    cliente = models.ForeignKey(ModeloCliente, on_delete=models.CASCADE)  
    fecha_solicitud = models.DateTimeField(auto_now_add=True) 
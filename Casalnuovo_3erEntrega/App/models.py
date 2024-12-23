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

# Modelo Compra
class ModeloCompra(models.Model):
    producto = models.ForeignKey(ModeloProducto, on_delete=models.CASCADE)  # Relación con Producto
    cantidad = models.PositiveIntegerField()  # Cantidad de productos comprados
    precio = models.DecimalField(max_digits=10, decimal_places=2)  # Precio total de la compra
    nro_compra = models.CharField(max_length=20, unique=True)  # Número de compra único

    def __str__(self):
        return f"Compra {self.nro_compra} - {self.producto.descripcion}"

# Modelo Reseña
class ModeloReseña(models.Model):
    cliente = models.ForeignKey(ModeloCliente, on_delete=models.CASCADE, related_name="reseñas")  # Relación con Cliente
    producto = models.ForeignKey(ModeloProducto, on_delete=models.CASCADE, related_name="reseñas")  # Relación con Producto
    comentario = models.TextField()

class SolicitudProductoFueraStock(models.Model):
    producto = models.CharField(max_length=255)  # Nombre del producto solicitado
    descripcion = models.TextField()  # Descripción opcional sobre el por qué lo buscan
    cliente = models.ForeignKey(ModeloCliente, on_delete=models.CASCADE)  
    fecha_solicitud = models.DateTimeField(auto_now_add=True) 

# Create your tests here.
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User  # Importa el modelo User para crear un usuario
from App.models import ModeloCliente

class ClienteTestCase(TestCase):

    def setUp(self):
        # Crear un usuario para probar la autenticación
        self.user = User.objects.create_user(username='testuser', password='12345')
        
        # Crear un cliente para probar
        self.cliente = ModeloCliente.objects.create(
            nombre="Juan",
            apellido="Perez",
            dni="12345678",
            direccion="Calle Ficticia 123",
            celular="555123456"
        )

    def test_eliminar_cliente(self):
        # Autenticamos al usuario para asegurarnos de que está autenticado
        self.client.login(username='testuser', password='12345')
        
        # Verificar que el cliente se ha creado correctamente
        self.assertEqual(ModeloCliente.objects.count(), 1)  # Asegurarse de que hay un cliente

        # Realizar la solicitud para eliminar el cliente
        response = self.client.post(reverse('eliminar_cliente', args=[self.cliente.id]))

        # Verificar que el cliente ha sido eliminado
        self.assertEqual(ModeloCliente.objects.count(), 0)

        # Verificar la redirección después de la eliminación
        self.assertEqual(response.status_code, 302)  # Verifica que la redirección funcione
        self.assertRedirects(response, reverse('buscar_cliente'))  # Verifica que redirige a 'buscar_cliente'

    def test_no_permitir_eliminar_cliente_no_autenticado(self):
        """Verificar que no se puede eliminar un cliente si no estás autenticado"""
        # Simulamos una petición sin haber iniciado sesión
        self.client.logout()
        
        response = self.client.post(reverse('eliminar_cliente', args=[self.cliente.id]))

        # Asegurarse de que se redirige a la página de login
        self.assertRedirects(response, reverse('Login') + '?next=' + reverse('eliminar_cliente', args=[self.cliente.id]))

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from App.models import ModeloCompra, ModeloProducto

class CompraTestCase(TestCase):

    def setUp(self):
        # Crear un producto de ejemplo
        self.producto = ModeloProducto.objects.create(
            descripcion="Producto de prueba", 
            precio=100.00, 
            stock=10
        )
        
        # Crear un cliente y un admin
        self.user = User.objects.create_user(username='usuario', password='password')
        self.admin = User.objects.create_user(username='admin', password='password', is_staff=True)
        
        # Crear una compra para ambos usuarios
        self.compra_user = ModeloCompra.objects.create(
            producto=self.producto,
            cantidad=1,
            precio=100.00,
            nro_compra="12345",
            usuario=self.user
        )
        
        self.compra_admin = ModeloCompra.objects.create(
            producto=self.producto,
            cantidad=1,
            precio=100.00,
            nro_compra="54321",
            usuario=self.admin
        )

    def test_eliminar_compra_admin(self):
        # Iniciar sesión como admin
        self.client.login(username='admin', password='password')
        
        # Hacer la solicitud de eliminación
        response = self.client.post(reverse('eliminar_compra', args=[self.compra_admin.id]))

        # Verificar que la compra ha sido eliminada
        self.assertEqual(ModeloCompra.objects.count(), 1)
        self.assertEqual(response.status_code, 302)  # Redirección a 'bienvenido'
        
    def test_no_permitir_eliminar_compra_no_admin(self):
        # Iniciar sesión como un usuario normal
        self.client.login(username='usuario', password='password')
        
        # Intentar eliminar una compra
        response = self.client.post(reverse('eliminar_compra', args=[self.compra_user.id]))

        # Verificar que la compra no se eliminó
        self.assertEqual(ModeloCompra.objects.count(), 2)  # Aún deberían existir las compras
        self.assertEqual(response.status_code, 302)  # Redirección a la página de bienvenida

# tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from App.models import ModeloProducto

class ProductoTestCase(TestCase):

    def setUp(self):
        # Crear un producto de ejemplo
        self.producto = ModeloProducto.objects.create(
            sku="12345",
            descripcion="Producto de prueba",
            precio=100.00,
            stock=10
        )
        
        # Crear un cliente (usuario normal) y un admin
        self.user = User.objects.create_user(username='usuario', password='password')
        self.admin = User.objects.create_user(username='admin', password='password', is_staff=True)

    def test_eliminar_producto_admin(self):
        # Iniciar sesión como admin
        self.client.login(username='admin', password='password')
        
        # Hacer la solicitud de eliminación
        response = self.client.post(reverse('eliminar_producto', args=[self.producto.sku]))
        
        # Verificar que el producto ha sido eliminado
        self.assertEqual(ModeloProducto.objects.count(), 0)  # Producto eliminado
        self.assertEqual(response.status_code, 302)  # Redirección a la página de bienvenida

    def test_no_permitir_eliminar_producto_no_admin(self):
        # Iniciar sesión como un usuario normal
        self.client.login(username='usuario', password='password')
        
        # Verificar que el producto existe antes de intentar eliminarlo
        productos_antes = ModeloProducto.objects.count()
        print("Productos antes de la eliminación:", productos_antes)  # Debe ser 1
        
        # Intentar eliminar el producto
        response = self.client.post(reverse('eliminar_producto', args=[self.producto.sku]))
        
        # Verificar que el producto no se ha eliminado
        productos_despues = ModeloProducto.objects.count()
        print("Productos después de la eliminación:", productos_despues)  # Debe seguir siendo 1
        
        # Verificar que el número de productos no cambió
        self.assertEqual(productos_despues, productos_antes)
        
        # Verificar que el código de estado sea 404
        self.assertEqual(response.status_code, 404)  # El acceso está restringido para usuarios no admin



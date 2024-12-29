from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

def inicio(request):
    return render(request, "App/inicio.html")

def clientes(request):
    return render(request, "App/clientes.html")

def productos(request):
    # Obtener todos los productos desde la base de datos
    productos = ModeloProducto.objects.all()
    
    return render(request, 'App/productos.html', {'productos': productos})

@login_required
def compra(request):
    return render(request, "App/compra.html")

def resenas(request):
    reseñas = ModeloReseña.objects.all()
    return render(request, 'App/resenas.html', {'reseñas': reseñas})
    


from django.shortcuts import render, redirect
from .forms import ModeloClienteForm

def clientes_formulario(request):
    if request.method == 'POST':
        form = ModeloClienteForm(request.POST)
        
        if form.is_valid():
            # Guardar los datos 
            form.save()

            return redirect('inicio') 

    else:
        form = ModeloClienteForm()

    return render(request, 'App/clientes_formulario.html', {'form': form})

from django.shortcuts import render, redirect
from .forms import ReseñaForm
from .models import ModeloReseña


def formulario_resena(request):
    if request.method == 'POST':
        form = ReseñaForm(request.POST)
        if form.is_valid():
            form.save() 
            return redirect('resenas')  # Redirige a la página de reseñas

    else:
        form = ReseñaForm()

    reseñas = ModeloReseña.objects.all()  

    return render(request, 'App/formulario-resena.html', {'form': form, 'reseñas': reseñas})

from django.shortcuts import render, redirect
from .forms import CompraForm
from django.contrib.auth.decorators import login_required

@login_required
def formulario_compra(request):
    if request.method == 'POST':
        form = CompraForm(request.POST)
        if form.is_valid():
            compra = form.save(commit=False)
            compra.usuario = request.user  # Asocia la compra con el usuario logueado
            compra.save()
            return redirect('bienvenido')  # Redirige a la página de compras del usuario
    else:
        form = CompraForm()

    return render(request, 'App/formulario-compra.html', {'form': form})
from django.shortcuts import render, redirect
from .forms import SolicitudProductoForm
from .models import SolicitudProductoFueraStock

def formulario_producto_fuera_stock(request):
    if request.method == 'POST':
        form = SolicitudProductoForm(request.POST)
        if form.is_valid():
            form.save()  # Guardar la solicitud en la base de datos
            return redirect('inicio')  # Redirigir a una página después de que la solicitud se haya guardado
    else:
        form = SolicitudProductoForm()

    return render(request, 'App/formulario-prodsinstock.html', {'form': form})

from django.shortcuts import render
from .models import ModeloCliente
from .forms import BusquedaClienteForm

def buscar_cliente(request):
    form = BusquedaClienteForm(request.GET)
    clientes = ModeloCliente.objects.all()

    if form.is_valid():
        nombre = form.cleaned_data.get('nombre')
        apellido = form.cleaned_data.get('apellido')
        email = form.cleaned_data.get('email')

        if nombre:
            clientes = clientes.filter(nombre__icontains=nombre)
        if apellido:
            clientes = clientes.filter(apellido__icontains=apellido)
        if email:
            clientes = clientes.filter(email__icontains=email)

    return render(request, "App/buscar_cliente.html", {'form': form, 'clientes': clientes})

from django.shortcuts import render
from .models import ModeloProducto
from .forms import BusquedaProductoForm

def buscar_producto(request):
    productos = None
    form = BusquedaProductoForm(request.GET)  # Usamos GET para recuperar los filtros de búsqueda

    if request.method == 'GET' and form.is_valid():
        descripcion = form.cleaned_data.get('descripcion')
        sku = form.cleaned_data.get('sku')
        precio_min = form.cleaned_data.get('precio_min')
        precio_max = form.cleaned_data.get('precio_max')

        productos = ModeloProducto.objects.all()

        # Aplicamos los filtros de búsqueda
        if descripcion:
            productos = productos.filter(descripcion__icontains=descripcion)  # Filtra por descripción que contenga el texto
        if sku:
            productos = productos.filter(sku__icontains=sku)  # Filtra por SKU que contenga el texto
        if precio_min is not None:
            productos = productos.filter(precio__gte=precio_min)  # Filtra por precio mayor o igual al mínimo
        if precio_max is not None:
            productos = productos.filter(precio__lte=precio_max)  # Filtra por precio menor o igual al máximo

    return render(request, 'App/buscar_producto.html', {'form': form, 'productos': productos})

from django.shortcuts import render, get_object_or_404, redirect
from .forms import ModeloClienteForm
from .models import ModeloCliente

def actualizar_cliente(request, cliente_dni):
    try:
        # Buscar el cliente por el DNI
        cliente = ModeloCliente.objects.get(dni=cliente_dni)
    except ModeloCliente.DoesNotExist:
        # Si no existe, lanzar un error 404 con un mensaje personalizado
        return render(request, 'App/cliente_no_encontrado.html', {'dni': cliente_dni})

    if request.method == 'POST':
        form = ModeloClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('inicio')
    else:
        form = ModeloClienteForm(instance=cliente)

    return render(request, 'App/actualizar_cliente.html', {'form': form, 'cliente': cliente})

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .models import ModeloProducto
from .forms import ModeloProductoForm

@login_required  # Asegura que el usuario esté logueado
def actualizar_producto(request, sku):
    # Verifica si el usuario es administrador
    if not request.user.is_staff:
        return HttpResponseForbidden("No tienes permisos para actualizar productos.")
    
    # Buscar el producto por el SKU
    producto = get_object_or_404(ModeloProducto, sku=sku)
    
    if request.method == 'POST':
        form = ModeloProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()  # Guardamos los cambios realizados al producto
            return redirect('productos')  # Redirigimos a la página de productos
    else:
        form = ModeloProductoForm(instance=producto)  # Cargamos el formulario con los datos actuales del producto

    return render(request, 'App/actualizar_producto.html', {'form': form, 'producto': producto})


from django.contrib.auth.decorators import login_required
from .models import ModeloProducto
from .forms import ModeloProductoForm

@login_required
def actualizar_producto(request, sku):
    # Verificar si el usuario es admin
    if not request.user.is_staff:
        return redirect('productos')  # Redirigir a la lista de productos si no es admin
    
    producto = get_object_or_404(ModeloProducto, sku=sku)

    if request.method == 'POST':
        form = ModeloProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()  # Guardamos los cambios realizados al producto
            return redirect('productos')  # Redirigimos a la página de productos
    else:
        form = ModeloProductoForm(instance=producto)  # Cargamos el formulario con los datos actuales del producto

    return render(request, 'App/actualizar_producto.html', {'form': form, 'producto': producto})



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ModeloProducto

@login_required
def eliminar_producto(request, sku):
    # Verificar si el usuario es admin
    if not request.user.is_staff:
        return redirect('productos')  # Redirigir a la lista de productos si no es admin

    producto = get_object_or_404(ModeloProducto, sku=sku)

    if request.method == 'POST':
        producto.delete()  # Eliminar el producto
        return redirect('productos')  # Redirigir a la lista de productos después de eliminar

    return render(request, 'App/eliminar_producto.html', {'producto': producto})

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from .models import ModeloProducto
from .forms import ModeloProductoForm 
# Vista para listar productos
class ProductoListView(ListView):
    model = ModeloProducto
    template_name = 'App/productos.html'  
    context_object_name = 'productos' 

class ProductoDetailView(DetailView):
    model = ModeloProducto
    template_name = 'App/producto_detail.html'
    context_object_name = 'producto'

    def get_object(self):
        # Aquí estamos utilizando el SKU en lugar del pk
        return get_object_or_404(ModeloProducto, sku=self.kwargs['sku'])

# Vista para actualizar un producto
class ProductoUpdateView(UpdateView):
    model = ModeloProducto
    form_class = ModeloProductoForm
    template_name = 'App/producto_form.html'
    context_object_name = 'producto'

    def get_object(self, queryset=None):
        # Aquí se usa `sku` para obtener el objeto del modelo
        return ModeloProducto.objects.get(sku=self.kwargs['sku'])

    def get_success_url(self):
        # Redirige a la lista de productos o a cualquier URL que desees después de actualizar
        return reverse_lazy('productos')
    
    # Vista para eliminar un producto
class ProductoDeleteView(DeleteView):
    model = ModeloProducto
    template_name = 'App/producto_confirm_delete.html'
    context_object_name = 'producto'

    def get_object(self, queryset=None):
        # Usa `sku` en lugar de `pk` para obtener el objeto del modelo
        return get_object_or_404(ModeloProducto, sku=self.kwargs['sku'])

    def get_success_url(self):
        # Redirige a la lista de productos después de eliminar
        return reverse_lazy('producto')

# views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ModeloCompra

@login_required
def bienvenido(request):
    # Obtener las compras del usuario logueado
    compras = ModeloCompra.objects.filter(usuario=request.user)

    return render(request, 'App/bienvenido.html', {'compras': compras})

from django.shortcuts import render

def about(request):
    return render(request, 'App/about.html')  # Asegúrate de que la ruta sea correcta

from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse

def inicio(request):
    return render(request, "App/inicio.html")

def clientes(request):
    return render(request, "App/clientes.html")

def productos(request):
    return render(request, "App/productos.html")

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
def formulario_compra(request):
    if request.method == 'POST':
        form = CompraForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda la compra en la base de datos
            return redirect('inicio')  # Redirige al inicio o a la página que desees
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

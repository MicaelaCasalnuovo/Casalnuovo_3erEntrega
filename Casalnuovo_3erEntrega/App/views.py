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
    return render(request, "App/compras.html")

def resenas(request):
    return render(request, "App/resenas.html")
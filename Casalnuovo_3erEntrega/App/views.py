from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse

def inicio(request):
    return HttpResponse("Vista inicio")

def clientes(request):
    return HttpResponse("Vista clientes")

def productos(request):
    return HttpResponse("Vista productos")

def compra(request):
    return HttpResponse("Vista compra")

def resenas(request):
    return HttpResponse("Vista reseñas")
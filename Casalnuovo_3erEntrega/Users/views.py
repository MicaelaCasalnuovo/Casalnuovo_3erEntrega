from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate

# Create your views here.
def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            usuario = form.cleaned_data.get('username')
            contra = form.cleaned_data.get('password')

            user = authenticate(username=usuario, password=contra)

            if user is not None:
                login(request, user)
                return render(request, "users/login.html", {'form': form})  # Ruta correcta
            else:
                return render(request, "users/login.html", {'mensaje': "Error, datos incorrectos"})
        else:
            return render(request, "users/login.html", {'mensaje': "Error, formulario erróneo"})
    else:
        form = AuthenticationForm()
    return render(request, "users/login.html", {'form': form})  # Ruta correcta

from django.shortcuts import render, redirect
from .forms import UserRegisterForm  # Importamos el formulario
from django.contrib.auth import login, authenticate

# Vista de registro
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)  # Usamos el formulario personalizado

        if form.is_valid():
            user = form.save()  # Guardar el usuario creado
            login(request, user)  # Loguear al usuario automáticamente después del registro
            return redirect('inicio')  # Redirigir al inicio o cualquier otra vista que prefieras
        else:
            return render(request, 'users/register.html', {'form': form, 'mensaje': 'Formulario incorrecto, verifica los datos.'})

    else:
        form = UserRegisterForm()  # Crear un formulario vacío para el primer GET
    return render(request, 'users/register.html', {'form': form})


# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.views import View

# Vista para manejar el logout
class CustomLogoutView(View):
    def get(self, request, *args, **kwargs):
        # Realizamos el logout
        logout(request)
        # Mostramos un mensaje de éxito
        messages.success(request, "Te has deslogueado correctamente.")
        # Redirigimos a la página de agradecimiento
        return redirect('GraciasPorVisitar')  # Redirige a la página "Gracias por visitar"

from django.shortcuts import render

from django.shortcuts import render

# Vista para la página de agradecimiento
def gracias_por_visitar(request):
    return render(request, "users/gracias_por_visitar.html")
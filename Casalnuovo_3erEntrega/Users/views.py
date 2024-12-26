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
                return render(request, "users/login.html", {'form': form}) 
            else:
                return render(request, "users/login.html", {'mensaje': "Error, datos incorrectos"})
        else:
            return render(request, "users/login.html", {'mensaje': "Error, formulario erróneo"})
    else:
        form = AuthenticationForm()
    return render(request, "users/login.html", {'form': form}) 
from django.shortcuts import render, redirect
from .forms import UserRegisterForm 
from django.contrib.auth import login, authenticate

# Vista de registro
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)  

        if form.is_valid():
            user = form.save()  
            login(request, user)  
            return redirect('inicio')  
        else:
            return render(request, 'users/register.html', {'form': form, 'mensaje': 'Formulario incorrecto, verifica los datos.'})

    else:
        form = UserRegisterForm()  # Crear un formulario vacío para el primer GET
    return render(request, 'users/register.html', {'form': form})


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
        return redirect('GraciasPorVisitar')  

from django.shortcuts import render

from django.shortcuts import render


def gracias_por_visitar(request):
    return render(request, "users/gracias_por_visitar.html")

# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import User

def cambiar_email_y_contrasena(request):
    if request.method == 'POST':
        
        email = request.POST.get('email')
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')

        # Validar usuario
        user = request.user
        if user.check_password(old_password):
            # Cambiar correo
            if email != user.email:
                user.email = email

            # Cambiar contraseña
            if new_password:
                user.set_password(new_password)
                update_session_auth_hash(request, user)  

            user.save()  # Guardar los cambios
            messages.success(request, 'Correo y/o contraseña cambiados exitosamente.')
            return redirect('perfil')  
        else:
            messages.error(request, 'Contraseña actual incorrecta.')
    
    return render(request, 'users/cambiar_email_y_contrasena.html')


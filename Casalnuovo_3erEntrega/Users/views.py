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

# users/views.py
# users/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from .forms import CambiarEmailYContrasenaForm
from django.contrib.auth.decorators import login_required

@login_required
def cambiar_email_y_contrasena(request):
    if request.method == 'POST':
        form = CambiarEmailYContrasenaForm(request.POST, request.FILES, instance=request.user)
        
        if form.is_valid():
            # Verificamos si la contraseña actual es correcta
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']

            # Verificar si la contraseña actual es correcta
            if request.user.check_password(old_password):
                # Cambiar contraseña si es necesario
                if new_password:
                    request.user.set_password(new_password)
                    update_session_auth_hash(request, request.user)  # Mantener la sesión activa

                # Guardar los cambios de email
                form.save()  # Esto guarda los cambios realizados en el formulario (por ejemplo, el email)

                # Si se subió una nueva imagen de avatar
                if 'imagen' in request.FILES:
                    avatar, created = Avatar.objects.get_or_create(user=request.user)  # Obtiene o crea un avatar para el usuario
                    avatar.imagen = request.FILES['imagen']
                    avatar.save()

                messages.success(request, 'Correo y/o contraseña cambiados exitosamente.')
                return redirect('perfil')  # Redirige a la página que desees (perfil del usuario, etc.)
            else:
                messages.error(request, 'La contraseña actual es incorrecta.')

    else:
        form = CambiarEmailYContrasenaForm(initial={'email': request.user.email})

    return render(request, 'users/cambiar_email_y_contrasena.html', {'form': form})
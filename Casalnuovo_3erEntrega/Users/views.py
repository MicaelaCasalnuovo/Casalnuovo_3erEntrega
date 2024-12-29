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

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from App.models import ModeloCliente


@login_required
def eliminar_cliente(request, id):
    cliente = get_object_or_404(ModeloCliente, id=id)
    
    # Verificar que el cliente se recuperó correctamente
    print(f"Intentando eliminar el cliente con ID {id}")
    
    cliente.delete()
    
    # Confirmación después de la eliminación
    print(f"Cliente con ID {id} eliminado.")
    
    return redirect('buscar_cliente')

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from App.models import ModeloCompra

@login_required
def eliminar_compra(request, id):
    # Verificar si el usuario es administrador
    if not request.user.is_staff:
        return redirect('bienvenido')  # O una página de error, si no es admin
    
    # Buscar la compra
    compra = get_object_or_404(ModeloCompra, id=id)
    
    # Eliminar la compra
    compra.delete()

    # Redirigir después de la eliminación
    return redirect('bienvenido')  # Redirige a la página de bienvenida o la que prefieras

# views.py


from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from App.models import ModeloProducto

# Vista para eliminar el producto solo si es admin
@login_required
def eliminar_producto(request, sku):
    # Obtener el producto por su SKU o lanzar error 404 si no existe
    producto = get_object_or_404(ModeloProducto, sku=sku)

    # Verificar si el usuario es admin
    if not request.user.is_staff:
        raise Http404("No tienes permisos para eliminar este producto.")  # Lanza un 404 si no es admin

    # Si el usuario es admin, proceder a eliminar
    producto.delete()

    # Redirigir a la página de bienvenida después de la eliminación
    return redirect('bienvenido')






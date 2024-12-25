# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Creamos el formulario de registro personalizado
class UserRegisterForm(UserCreationForm):
    # Puedes agregar otros campos si lo necesitas
    email = forms.EmailField()  # Campo para el correo electrónico

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']  # Campos a mostrar en el formulario

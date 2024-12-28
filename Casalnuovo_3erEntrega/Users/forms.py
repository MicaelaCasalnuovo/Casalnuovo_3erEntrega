# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegisterForm(UserCreationForm):
   
    email = forms.EmailField()  

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']  


# users/forms.py
# users/forms.py
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from .models import Avatar  

class CambiarEmailYContrasenaForm(UserChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput, required=True, label='Contraseña Actual')
    new_password = forms.CharField(widget=forms.PasswordInput, required=False, label='Nueva Contraseña')
    imagen = forms.ImageField(required=False, label='Avatar')  

    class Meta:
        model = User
        fields = ['username', 'email','imagen' ]
        help_texts = {field: "" for field in ['username', 'email', 'imagen']} 


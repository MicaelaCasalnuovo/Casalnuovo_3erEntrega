from django import forms
from .models import ModeloCliente
from .models import ModeloReseña
from .models import ModeloCliente, ModeloProducto

class ModeloClienteForm(forms.ModelForm):
    class Meta:
        model = ModeloCliente
        fields = ['nombre', 'apellido', 'dni', 'direccion', 'celular']

from django import forms
from .models import ModeloReseña
from .models import ModeloCliente, ModeloProducto

class ReseñaForm(forms.ModelForm):
    class Meta:
        model = ModeloReseña
        fields = ['cliente', 'producto', 'comentario']  

        widgets = {
            'comentario': forms.Textarea(attrs={'rows': 4, 'cols': 40}), 
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
      
        self.fields['cliente'].queryset = ModeloCliente.objects.all()
        self.fields['producto'].queryset = ModeloProducto.objects.all()

from django import forms
from .models import ModeloCompra

class CompraForm(forms.ModelForm):
    class Meta:
        model = ModeloCompra
        fields = ['producto', 'cantidad', 'precio', 'nro_compra']
        
        widgets = {
            'precio': forms.NumberInput(attrs={'step': '0.01'}),  # Para asegurar que el precio tenga decimales
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['producto'].queryset = ModeloProducto.objects.all()

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.usuario = self.initial.get('usuario')  # Asocia el usuario con la compra
        if commit:
            instance.save()
        return instance
    
    
from django import forms
from .models import SolicitudProductoFueraStock

class SolicitudProductoForm(forms.ModelForm):
    class Meta:
        model = SolicitudProductoFueraStock
        fields = ['producto', 'descripcion', 'cliente'] 

        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4, 'cols': 40}),  
        }

class BusquedaClienteForm(forms.Form):
    nombre = forms.CharField(max_length=100, required=False, label="Nombre del Cliente")
    apellido = forms.CharField(max_length=100, required=False, label="Apellido del Cliente")
    email = forms.EmailField(required=False, label="Correo Electrónico")

from django import forms

class BusquedaProductoForm(forms.Form):
    descripcion = forms.CharField(max_length=100, required=False, label="Descripción del Producto")
    sku = forms.CharField(max_length=50, required=False, label="SKU del Producto")
    precio_min = forms.DecimalField(max_digits=10, decimal_places=2, required=False, label="Precio Mínimo")
    precio_max = forms.DecimalField(max_digits=10, decimal_places=2, required=False, label="Precio Máximo")

from django import forms
from .models import ModeloProducto

class ModeloProductoForm(forms.ModelForm):
    class Meta:
        model = ModeloProducto
        fields = ['sku', 'descripcion', 'stock', 'precio']

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
        fields = ['cliente', 'producto', 'comentario']  # Campos del formulario

        widgets = {
            'comentario': forms.Textarea(attrs={'rows': 4, 'cols': 40}),  # Personalizando el widget para el comentario
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Opcional: puedes limitar los clientes y productos disponibles en los formularios si es necesario
        self.fields['cliente'].queryset = ModeloCliente.objects.all()
        self.fields['producto'].queryset = ModeloProducto.objects.all()

from django import forms
from .models import ModeloCompra
from .models import ModeloProducto

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

from django import forms
from .models import SolicitudProductoFueraStock

class SolicitudProductoForm(forms.ModelForm):
    class Meta:
        model = SolicitudProductoFueraStock
        fields = ['producto', 'descripcion', 'cliente']  # Campos que se van a mostrar en el formulario

        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4, 'cols': 40}),  # Personalizando el widget para la descripción
        }

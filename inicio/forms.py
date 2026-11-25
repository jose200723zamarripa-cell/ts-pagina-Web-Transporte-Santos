from django import forms
from .models import BitacoraCarga, Operador, Vehiculo, Viaje


class OperadorForm(forms.ModelForm):

  class Meta:
    model = Operador
    fields = ['nombre', 'telefono', 'licencia', 'tipo_licencia', 'estado']
    widgets = {
        'nombre': forms.TextInput(attrs={'class': 'form-control'}),
        'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        'licencia': forms.TextInput(attrs={'class': 'form-control'}),
        'tipo_licencia': forms.TextInput(attrs={'class': 'form-control'}),
        'estado': forms.Select(attrs={'class': 'form-control'}),
    }


class VehiculoForm(forms.ModelForm):

  class Meta:
    model = Vehiculo
    fields = ['placas', 'tipo', 'capacidad_carga_toneladas', 'estado']


class ViajeForm(forms.ModelForm):

  class Meta:
    model = Viaje
    fields = [
        'origen',
        'destino',
        'operador',
        'vehiculo',
        'fecha_salida',
        'fecha_llegada_estimada',
        'estado',
    ]
    widgets = {
        'fecha_salida': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        'fecha_llegada_estimada': forms.DateTimeInput(
            attrs={'type': 'datetime-local'}
        ),
    }
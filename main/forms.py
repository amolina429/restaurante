from django import forms
from .models import Pedido, DetallePedido, Plato

class PedidoBaseForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['tipo_documento', 'numero_documento', 'nombre_completo', 'celular', 'email']
        widgets = {
            'tipo_documento': forms.Select(attrs={'class': 'form-select'}),
            'numero_documento': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_completo': forms.TextInput(attrs={'class': 'form-control'}),
            'celular': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class MesaForm(PedidoBaseForm):
    numero_mesa = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    
    class Meta(PedidoBaseForm.Meta):
        fields = PedidoBaseForm.Meta.fields + ['numero_mesa']

class DomicilioForm(PedidoBaseForm):
    direccion = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
    
    class Meta(PedidoBaseForm.Meta):
        fields = PedidoBaseForm.Meta.fields + ['direccion']

class RecogerForm(PedidoBaseForm):
    pass

class DetallePedidoForm(forms.ModelForm):
    plato = forms.ModelChoiceField(
        queryset=Plato.objects.filter(disponible=True),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    cantidad = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = DetallePedido
        fields = ['plato', 'cantidad', 'observaciones']
        widgets = {
            'observaciones': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Sin cebolla, sin picante, etc.'
            }),
        }

DetallePedidoFormSet = forms.inlineformset_factory(
    Pedido, DetallePedido, form=DetallePedidoForm,
    extra=1, can_delete=False, min_num=1, validate_min=True
)
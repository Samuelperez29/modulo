from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Producto


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.EmailInput(attrs={'placeholder': 'correo electronico'}))
    first_name = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'nombre'}))
    last_name = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'apellido'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'nombre de usuario'
        self.fields['username'].label = ''
        self.fields['username'].help_text = ('<span class="form-text text-muted"><small>Requerido. 150 caracteres o menos.</small></span>')

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'contrasena'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = ('<ul class="form-text text-muted"><li>Minimo 8 caracteres.</li></ul>')

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'confirmar contrasena'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = ('<ul class="form-text text-muted"><li>Ingrese la misma contrasena.</li></ul>')


class ProductoForm(forms.ModelForm):
    nombre = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'nombre del producto', 'class': 'form-control'}))
    cantidad = forms.IntegerField(label="", widget=forms.NumberInput(attrs={'placeholder': 'cantidad', 'class': 'form-control'}))
    descripcion = forms.CharField(required=False, label="", widget=forms.Textarea(attrs={'placeholder': 'descripcion (opcional)', 'class': 'form-control', 'rows': 3}))
    stock_minimo = forms.IntegerField(label="", widget=forms.NumberInput(attrs={'placeholder': 'stock minimo', 'class': 'form-control'}))
    estado = forms.ChoiceField(label="", choices=[('pendiente', 'Pendiente'), ('activo', 'Activo'), ('inactivo', 'Inactivo')], widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Producto
        fields = ['nombre', 'cantidad', 'descripcion', 'stock_minimo', 'estado']

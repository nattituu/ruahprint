from django import forms
from ..models import Producto, Categoria


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['codigo', 'nombre', 'descripcion', 'precio', 'categoria', 'imagen']
        widgets = {
            'codigo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: PROD01'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Etiquetas Textil'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe el producto...'
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'placeholder': 'Ej: 6990'
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-control'
            }),
        }

    def clean_codigo(self):
        codigo = self.cleaned_data.get('codigo', '').strip()
        if not codigo:
            raise forms.ValidationError('El código es obligatorio.')
        if len(codigo) < 3:
            raise forms.ValidationError('El código debe tener al menos 3 caracteres.')
        return codigo.upper()

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '').strip()
        if not nombre:
            raise forms.ValidationError('El nombre es obligatorio.')
        if len(nombre) < 3:
            raise forms.ValidationError('El nombre debe tener al menos 3 caracteres.')
        return nombre

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio is None:
            raise forms.ValidationError('El precio es obligatorio.')
        if precio <= 0:
            raise forms.ValidationError('El precio debe ser mayor a 0.')
        if precio > 10000000:
            raise forms.ValidationError('El precio parece demasiado alto. Verifícalo.')
        return precio

    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion', '').strip()
        if not descripcion:
            raise forms.ValidationError('La descripción es obligatoria.')
        if len(descripcion) < 10:
            raise forms.ValidationError('La descripción debe tener al menos 10 caracteres.')
        return descripcion


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['codigo', 'nombre']
        widgets = {
            'codigo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: TEXTI'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Textil'
            }),
        }

    def clean_codigo(self):
        codigo = self.cleaned_data.get('codigo', '').strip()
        if not codigo:
            raise forms.ValidationError('El código es obligatorio.')
        if len(codigo) < 2:
            raise forms.ValidationError('El código debe tener al menos 2 caracteres.')
        return codigo.upper()

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '').strip()
        if not nombre:
            raise forms.ValidationError('El nombre es obligatorio.')
        if len(nombre) < 2:
            raise forms.ValidationError('El nombre debe tener al menos 2 caracteres.')
        return nombre
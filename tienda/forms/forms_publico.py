from django import forms


class FormularioContacto(forms.Form):
    nombre = forms.CharField(
        label="Tu Nombre",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Marcela Pérez'})
    )
    correo = forms.EmailField(
        label="Tu Correo",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ejemplo@correo.com'})
    )
    asunto = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Consulta etiquetas ropa'})
    )
    mensaje = forms.CharField(
        label="Mensaje",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Cuéntanos qué necesitas...'})
    )
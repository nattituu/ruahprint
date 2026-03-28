from django import forms
from ..models import MenuAcceso


class MenuAccesoForm(forms.ModelForm):
    class Meta:
        model = MenuAcceso
        fields = ['codigo', 'texto', 'perfil', 'padre']
        widgets = {
            'padre': forms.Select(attrs={'class': 'form-control'})
        }
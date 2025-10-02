from django import forms
from .models import ClinicInfo

class ClinicInfoForm(forms.ModelForm):
    class Meta:
        model = ClinicInfo
        fields = ['name', 'slogan', 'logo', 'primary_color', 'secondary_color', 'background_color']
        labels = {
            'name': 'Nom du cabinet',
            'slogan': 'Slogan / Sous-titre',
            'logo': 'Logo du cabinet',
            'primary_color': 'Couleur principale',
            'secondary_color': 'Couleur secondaire',
            'background_color': 'Couleur de fond'
        }
        widgets = {
            'primary_color': forms.TextInput(attrs={'type': 'color'}),
            'secondary_color': forms.TextInput(attrs={'type': 'color'}),
            'background_color': forms.TextInput(attrs={'type': 'color'}),
        }

from django import forms
from .models import ClinicInfo

class ClinicInfoForm(forms.ModelForm):
    class Meta:
        model = ClinicInfo
        fields = [
            'name', 'slogan', 'logo',
            'address', 'phone', 'email',
            'primary_color', 'secondary_color', 'background_color', 'font_family',
            'facebook', 'instagram', 'linkedin',
            'show_logo', 'show_slogan', 'dark_mode_enabled', 'opening_hours'
        ]
        labels = {
            'name': 'Nom du cabinet',
            'slogan': 'Slogan / Sous-titre',
            'logo': 'Logo du cabinet',
            'primary_color': 'Couleur principale',
            'secondary_color': 'Couleur secondaire',
            'background_color': 'Couleur de fond',
            'font_family': 'Police du site',
        }
        widgets = {
            'primary_color': forms.TextInput(attrs={'type': 'color', 'class': 'form-control form-control-color'}),
            'secondary_color': forms.TextInput(attrs={'type': 'color', 'class': 'form-control form-control-color'}),
            'background_color': forms.TextInput(attrs={'type': 'color', 'class': 'form-control form-control-color'}),
            'opening_hours': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ex : Lundi-Vendredi 09h-18h'}),
            'font_family': forms.Select(choices=[
                ('Arial, sans-serif', 'Arial'),
                ('"Times New Roman", serif', 'Times New Roman'),
                ('"Open Sans", sans-serif', 'Open Sans'),
                ('Roboto, sans-serif', 'Roboto'),
                ('Georgia, serif', 'Georgia'),
            ]),
        }

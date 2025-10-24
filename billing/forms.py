from django import forms
from .models import Billing,ClinicHeader

class BillingForm(forms.ModelForm):
    class Meta:
        model = Billing
        fields = ['appointment', 'amount', 'paid']
        labels = {
            'appointment': 'Rendez-vous',
            'amount': 'Montant (€)',
            'paid': 'Payée ?'
        }
        widgets = {
            # Pour avoir un rendu Bootstrap plus joli
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'appointment': forms.Select(attrs={'class': 'form-select'}),
            'paid': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class HeaderForm(forms.ModelForm):
    class Meta:
        model = ClinicHeader
        fields = ['logo', 'header_text']
        widgets = {
            'header_text': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Texte de l’en-tête...'}),
        }

from django import forms
from .models import Patient

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        exclude = ['medecin']  # on affecte le médecin automatiquement


from django import forms
from .models import Patient

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        exclude =['medecin']
        fields = [
            "first_name",
            "last_name",
            "date_of_birth",
            "phone",
            "email",
            "address",
            "medical_history",
        ]

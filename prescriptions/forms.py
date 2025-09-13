# prescriptions/forms.py
from django import forms
from .models import Prescription

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ["text"]
        labels = {"text": "Prescription"}

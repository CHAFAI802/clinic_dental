from django import forms
from prescriptions.models import Prescription 

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ["appointment", "text"]  # <-- ajouter appointment ici
        labels = {
            "appointment": "Rendez-vous",
            "text": "Texte de l'ordonnance"
        }
        widgets = {
            "appointment": forms.Select(attrs={"class": "form-control"}),
            "text": forms.Textarea(attrs={"class": "form-control"})
        }


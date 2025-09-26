from django import forms
from .models import Prescription, PrescriptionItem
from appointments.models import Appointment
from django.forms import inlineformset_factory


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ["appointment", "text"]  # le champ created_at est automatique
        labels = {
            "appointment": "Rendez-vous",
            "text": "Texte de l'ordonnance",
        }
        widgets = {
            "appointment": forms.Select(attrs={"class": "form-control"}),
            "text": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "Écrire le contenu de l'ordonnance ici..."
            }),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # possibilité de filtrer par médecin connecté
        super().__init__(*args, **kwargs)
        if user is not None and 'appointment' in self.fields:
            # On restreint les rendez-vous affichés à ceux du médecin connecté
            self.fields['appointment'].queryset = Appointment.objects.filter(medecin=user)

class PrescriptionItemForm(forms.ModelForm):
    class Meta:
        model = PrescriptionItem
        fields = ['medicament', 'posologie', 'quantite', 'unite']
        widgets = {
            'medicament': forms.TextInput(attrs={'class': 'form-control'}),
            'posologie': forms.TextInput(attrs={'class': 'form-control'}),
            'quantite': forms.NumberInput(attrs={'class': 'form-control'}),
            'unite': forms.TextInput(attrs={'class': 'form-control'}),
        }

PrescriptionItemFormSet = inlineformset_factory(
    Prescription,
    PrescriptionItem,
    form=PrescriptionItemForm,
    extra=1,
    can_delete=True
)

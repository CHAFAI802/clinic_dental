from django import forms
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from datetime import timedelta
from .models import Appointment
from patients.models import Patient


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["patient", "datetime", "reason", "status","medecin"]
        widgets = {
            "datetime": forms.DateTimeInput(
                attrs={"type": "datetime-local", "class": "form-control"}
            ),
            "reason": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "patient": forms.Select(attrs={"class": "form-select"}),
            "medecin": forms.Select(attrs={"class": "form-select"}),  # visible par défaut
        }

    def __init__(self, *args, user=None, **kwargs):
        user = kwargs.pop("user", None)   # récupère l’utilisateur injecté
        super().__init__(*args, **kwargs)

        if user and user.role=="medecin":
                # Champ caché et pré-rempli
            self.fields["medecin"].widget = forms.HiddenInput()
            self.initial["medecin"] = user  

        elif  user and user.role ==["secretaire","admin"]:
                # Restreindre aux médecins
            self.fields["medecin"].queryset = (get_user_model().objects.filter(role="medecin"))

                
        def clean(self):
            cleaned_data = super().clean()
            patient = cleaned_data.get("patient")
            dt = cleaned_data.get("datetime")
            medecin = cleaned_data.get("medecin") or getattr(self.instance, "medecin", None)

            # Attribution automatique du médecin
            if medecin is None:
                if self.user and getattr(self.user, "role", None) == "medecin":
                    medecin = self.user
                elif patient and getattr(patient, "medecin", None):
                    medecin = patient.medecin

            if medecin is None:
                raise ValidationError("Impossible de déterminer le médecin pour ce rendez-vous.")

            # Empêcher RDV passé
            if dt and dt < timezone.now():
                raise ValidationError("Impossible de programmer un rendez-vous dans le passé.")

            # Vérifier conflits sur 20 minutes
            if patient and dt:
                start_window = dt - timedelta(minutes=20)
                end_window = dt + timedelta(minutes=20)

                conflict = Appointment.objects.filter(
                medecin=medecin,
                datetime__range=(start_window, end_window)
                ).exclude(pk=self.instance.pk)

                if conflict.exists():
                    raise ValidationError(
                    "Ce médecin a déjà un autre patient programmé dans les 20 minutes autour de ce rendez-vous."
                    )

            # Synchronisation
            cleaned_data["medecin"] = medecin
            self.instance.medecin = medecin

            return cleaned_data

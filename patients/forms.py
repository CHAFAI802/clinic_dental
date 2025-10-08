# patients/forms.py
from django import forms
from .models import Patient
from accounts.models import CustomUser

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        exclude = []  # on va gérer l’exclusion conditionnelle

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if user:
            if user.is_secretaire():
                # La secrétaire peut choisir le médecin
                self.fields['medecin'].queryset = CustomUser.objects.filter(role='medecin')
            else:
                # Médecin : on n’affiche pas le champ medecin
                self.fields.pop('medecin', None)

from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.conf import settings



class ClinicInfo(models.Model):
    name = models.CharField("Nom du cabinet", max_length=255)
    slogan = models.CharField("Slogan / Sous-titre", max_length=255, blank=True)
    logo = models.ImageField("Logo du cabinet", upload_to="clinic_logos/", blank=True, null=True)

    address = models.CharField("Adresse", max_length=255, blank=True)
    phone = models.CharField("Téléphone", max_length=50, blank=True)
    email = models.EmailField("Email", blank=True)

    primary_color = models.CharField("Couleur principale", max_length=7, default="#0d6efd")
    secondary_color = models.CharField("Couleur secondaire", max_length=7, default="#6c757d")
    background_color = models.CharField("Couleur de fond", max_length=7, default="#ffffff")
    font_family = models.CharField("Police du site", max_length=100, default="Arial, sans-serif")

    facebook = models.URLField("Facebook", blank=True)
    instagram = models.URLField("Instagram", blank=True)
    linkedin = models.URLField("LinkedIn", blank=True)

    show_logo = models.BooleanField("Afficher le logo", default=True)
    show_slogan = models.BooleanField("Afficher le slogan", default=True)
    dark_mode_enabled = models.BooleanField("Activer le mode sombre", default=False)
    opening_hours = models.TextField("Horaires d'ouverture", blank=True)

    class Meta:
        verbose_name = "Information du cabinet"
        verbose_name_plural = "Informations du cabinet"

    def clean(self):
        if not self.pk and ClinicInfo.objects.exists():
            raise ValidationError("Il ne peut y avoir qu'une seule configuration du cabinet.")

    def __str__(self):
        return self.name

# core/models.py
class ActionLog(models.Model):
    ACTION_TYPES = [
        ("SUPPRESSION_PATIENT", "Suppression de patient"),
        ("RESTAURATION_PATIENT", "Restauration de patient"),
    ]

    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="actions_logs",
    )
    action_type = models.CharField(max_length=50, choices=ACTION_TYPES)
    patient_last_name = models.CharField(max_length=100)
    patient_id = models.IntegerField(null=True, blank=True)
    horodatage = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.get_action_type_display()} - {self.patient_last_name} ({self.horodatage:%d/%m/%Y %H:%M})"

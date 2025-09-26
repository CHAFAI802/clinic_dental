# prescriptions/models.py
from django.db import models
from django.utils import timezone
from appointments.models import Appointment  

class Prescription(models.Model):
    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.CASCADE,
        related_name='prescriptions',
        verbose_name="Rendez-vous"
    )
    text = models.TextField("Texte de l’ordonnance", blank=True)
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Créée le"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Ordonnance"
        verbose_name_plural = "Ordonnances"

    def __str__(self):
        return f"Ordonnance pour {self.appointment.patient}"

# ---- Nouveau modèle pour les lignes de prescription ----
class PrescriptionItem(models.Model):
    prescription = models.ForeignKey(
        Prescription,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Ordonnance"
    )
    medicament = models.CharField("Nom du médicament", max_length=255)
    posologie = models.CharField("Posologie", max_length=255)
    quantite = models.PositiveIntegerField("Quantité")
    unite = models.CharField(
        "Unité",
        max_length=100,
        help_text="Ex: boîte, flacon, injection, suppositoire…"
    )

    class Meta:
        verbose_name = "Médicament prescrit"
        verbose_name_plural = "Médicaments prescrits"

    def __str__(self):
        return f"{self.medicament} – {self.posologie} ({self.quantite} {self.unite})"

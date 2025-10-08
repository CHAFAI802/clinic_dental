from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta

from patients.models import Patient


class Appointment(models.Model):
    STATUS_SCHEDULED = "scheduled"
    STATUS_COMPLETED = "completed"
    STATUS_CANCELED = "canceled"
    STATUS_PRESENT = "present"

    STATUS_CHOICES = [
        (STATUS_SCHEDULED, "Planifié"),
        (STATUS_PRESENT, "Présent"),
        (STATUS_COMPLETED, "Terminé"),
        (STATUS_CANCELED, "Annulé"),
    ]

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="appointments",
        verbose_name="Patient"
    )
    medecin = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={"role": "medecin"},
        related_name="appointments_medecin",
        verbose_name="Médecin"
    )
    datetime = models.DateTimeField("Date et heure du rendez-vous")  # 👈 un seul champ
    reason = models.TextField("Motif", blank=True, null=True)
    done = models.BooleanField(default=False, verbose_name="Rendez-vous effectué")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_SCHEDULED,
        verbose_name="Statut"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-datetime"]
        verbose_name = "Rendez-vous"
        verbose_name_plural = "Rendez-vous"

    def __str__(self):
        return f"{self.patient} - {self.datetime.strftime('%d/%m/%Y %H:%M')} ({self.get_status_display()})"

    def clean(self):
        super().clean()

        if not self.datetime:
            return

        dt_rdv = self.datetime
        if timezone.is_naive(dt_rdv):
            dt_rdv = timezone.make_aware(dt_rdv)

        # Vérif : pas dans le passé
        if dt_rdv < timezone.now():
            raise ValidationError("La date et l'heure du rendez-vous ne peuvent pas être dans le passé.")

        # Vérif : chevauchement 20 min
        overlap_start = dt_rdv
        overlap_end = dt_rdv + timedelta(minutes=20)

        overlap = Appointment.objects.filter(
            medecin=self.medecin,
            datetime__gte=overlap_start,
            datetime__lt=overlap_end,
        ).exclude(pk=self.pk)

        if overlap.exists():
            raise ValidationError(
                "Ce médecin a déjà un rendez-vous dans cette tranche de 20 minutes."
            )

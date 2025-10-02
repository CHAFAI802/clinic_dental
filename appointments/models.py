from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime, timedelta
from patients.models import Patient
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class Appointment(models.Model):
    STATUS_SCHEDULED = "scheduled"
    STATUS_COMPLETED = "completed"
    STATUS_CANCELED = "canceled"

    STATUS_CHOICES = [
        (STATUS_SCHEDULED, "Planifié"),
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
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={"role": "medecin"},
        related_name="appointments_medecin",
        verbose_name="Médecin"
    )
    date = models.DateField("Date du rendez-vous")
    time = models.TimeField("Heure du rendez-vous")
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
        ordering = ["-date", "-time"]
        verbose_name = "Rendez-vous"
        verbose_name_plural = "Rendez-vous"

    def __str__(self):
        return f"{self.patient} - {self.date} {self.time} ({self.get_status_display()})"

    def clean(self):
        """Validation métier : pas de date passée, pas de chevauchement < 15 min pour un médecin"""
        dt_rdv = datetime.combine(self.date, self.time)

        # 1. Pas de rendez-vous dans le passé
        if dt_rdv < timezone.now():
            raise ValidationError("La date et l'heure du rendez-vous ne peuvent pas être dans le passé.")

        # 2. Vérifier les chevauchements pour le même médecin
        conflicts = Appointment.objects.filter(
            medecin=self.medecin,
            date=self.date
        )

        if self.pk:
            conflicts = conflicts.exclude(pk=self.pk)

        for rdv in conflicts:
            rdv_dt = datetime.combine(rdv.date, rdv.time)
            delta = abs((rdv_dt - dt_rdv).total_seconds()) / 60  # différence en minutes
            if delta < 15:
                raise ValidationError("Un autre rendez-vous est déjà prévu dans les 15 minutes pour ce médecin.")

from django.db import models
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
        related_name="appointments"
    )
    medecin = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={"role": "medecin"}
    )
    date = models.DateField()
    time = models.TimeField()
    reason = models.TextField(blank=True, null=True)
    done = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_SCHEDULED
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date", "-time"]
        verbose_name = "Rendez-vous"
        verbose_name_plural = "Rendez-vous"

    def __str__(self):
        return f"{self.patient} - {self.date} {self.time} ({self.get_status_display()})"

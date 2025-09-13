# prescriptions/models.py
from django.db import models
from appointments.models import Appointment  

class Prescription(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return f"Ordonnance pour {self.appointment.patient}"

from django.db import models
from appointments.models import Appointment  


class Billing(models.Model):
    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.CASCADE,
        related_name='billing'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)
    issued_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Facture RDV {self.appointment.id} - {self.amount}€"
    

class ClinicHeader(models.Model):
    logo = models.ImageField(upload_to='headers/', blank=True, null=True)
    header_text = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.header_text or "En-tête du cabinet"
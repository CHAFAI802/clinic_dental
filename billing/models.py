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
    


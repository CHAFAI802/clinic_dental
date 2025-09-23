from django.db import models
from accounts.models import CustomUser

class Patient(models.Model):
    medecin = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='patients',
        limit_choices_to={'role': 'medecin'}
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    phone = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    medical_history = models.TextField(blank=True, null=True)
    consultation_fee = models.DecimalField(  # <-- ajouté
        max_digits=10, decimal_places=2, default=500.00,
        help_text="Tarif standard de consultation"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"



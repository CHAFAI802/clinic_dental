from django.db import models
from accounts.models import CustomUser  # <-- importe ton user

class Patient(models.Model):
    # nouveau champ : le médecin propriétaire du patient
    medecin = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="patients",
        limit_choices_to={'role': 'medecin'}  # optionnel pour limiter aux médecins
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    phone = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True, null=True, default=None, blank=True)
    address = models.TextField(blank=True, null=True)
    medical_history = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

from django.db import models
from django.utils import timezone
from django.db.models import Q
from accounts.models import CustomUser  # ajuste selon ton arborescence

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
    consultation_fee = models.DecimalField(
        max_digits=10, decimal_places=2, default=500.00,
        help_text="Tarif standard de consultation"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    actif = models.BooleanField(default=True)
    date_suppression = models.DateTimeField(blank=True, null=True)

    def supprimer_logiquement(self, user=None):
        """Désactive le patient et journalise l’auteur."""
        self.__deleted_by = user
        self.actif = False
        self.date_suppression = timezone.now()
        self.first_name = "SUPPRIMÉ"
        self.last_name = ""
        self.email = ""
        self.phone = ""
        self.save()

    def restaurer(self, user=None):
        """Restaure un patient précédemment supprimé."""
        self._restored_by = user
        self.actif = True
        self.date_suppression = None
        self.save()

    def has_unpaid_bills(self):
        """Vérifie si le patient a au moins une facture non payée."""
        from billing.models import Billing
        return Billing.objects.filter(
            appointment__patient=self,
            paid=False
        ).exists()

    def __str__(self):
        status = "" if self.actif else " (inactif)"
        return f"{self.first_name} {self.last_name}{status}"

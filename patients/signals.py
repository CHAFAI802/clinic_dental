from django.db.models.signals import post_save
from django.dispatch import receiver
from appointments.models import Appointment
from billing.models import Billing
from .models import Patient


@receiver(post_save, sender=Appointment)
def create_or_update_billing(sender, instance, created, **kwargs):
    """
    Crée ou met à jour la facture associée à un rendez-vous.
    """
    patient = instance.patient
    amount = patient.consultation_fee or 0.00

    if created:
        # Créer la facture si elle n'existe pas
        Billing.objects.create(
            appointment=instance,
            amount=amount,
            paid=False
        )
    else:
        # Mettre à jour la facture existante si elle existe déjà
        if hasattr(instance, 'billing'):
            billing = instance.billing
            billing.amount = amount
            billing.save()



@receiver(post_save, sender=Patient)
def update_billings_when_patient_fee_changes(sender, instance, created, **kwargs):
    """
    Met à jour toutes les factures des rendez-vous futurs
    si le tarif du patient est modifié.
    """
    if not created:
        for appointment in instance.appointments.all():
            if hasattr(appointment, 'billing'):
                billing = appointment.billing
                billing.amount = instance.consultation_fee or 0.00
                billing.save()

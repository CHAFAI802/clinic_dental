from django.db.models.signals import post_save
from django.dispatch import receiver
from appointments.models import Appointment
from django.core.exceptions import PermissionDenied
from billing.models import Billing
from .models import Patient
from django.db.models.signals import pre_delete
from core.models import ActionLog


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


@receiver(pre_delete, sender=Patient)
def verifier_facturation_patient(sender, instance, **kwargs):
    """Empêche la suppression d’un patient avec des factures non payées."""
    if Billing.objects.filter(
        appointment__patient=instance,
        paid=False
    ).exists():
        raise PermissionDenied("Impossible de supprimer : ce patient a des factures impayées.")

@receiver(post_save, sender=Patient)
def log_patient_actions(sender, instance, **kwargs):
    """Journalise automatiquement les suppressions et restaurations."""
    if not instance.actif and hasattr(instance, "_deleted_by"):
        ActionLog.objects.create(
            utilisateur=instance._deleted_by,
            action_type="SUPPRESSION_PATIENT",
            patient_last_name=f"{instance.last_name}",
            patient_id=instance.id,
        )
    elif instance.actif and hasattr(instance, "_restored_by"):
        ActionLog.objects.create(
            utilisateur=instance._restored_by,
            action_type="RESTAURATION_PATIENT",
            patient_last_name=f"{instance.last_name}",
            patient_id=instance.id,
        )
from django.db.models.signals import post_save
from django.dispatch import receiver
from appointments.models import Appointment
from billing.models import Billing

@receiver(post_save, sender=Appointment)
def create_billing_on_presence(sender, instance, created, **kwargs):
    """
    Crée une facture uniquement lorsque le rendez-vous est marqué comme "présent"
    par la secrétaire, et non lors de la création du rendez-vous.
    """
    # On agit uniquement si le rendez-vous existait déjà et que le statut est "present"
    if not created and getattr(instance, "status", None) == "present":
        Billing.objects.get_or_create(
            appointment=instance,
            defaults={
                "amount": instance.patient.consultation_fee or 0.00,
                "confirmed_by_doctor": False,
                "confirmed_by_secretary": False,
                "is_confirmed": False,
            }
        )

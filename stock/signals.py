# stock/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum
from .models import Movement, Product

@receiver([post_save, post_delete], sender=Movement)
def update_product_stock(sender, instance, **kwargs):
    """Met à jour automatiquement current_stock après chaque mouvement."""
    product = instance.product
    entree = Movement.objects.filter(product=product, movement_type='IN').aggregate(total=Sum('quantity'))['total'] or 0
    sortie = Movement.objects.filter(product=product, movement_type='OUT').aggregate(total=Sum('quantity'))['total'] or 0
    curent_stock= product.quantity + entree - sortie
    product.save(update_fields=['quantity'])

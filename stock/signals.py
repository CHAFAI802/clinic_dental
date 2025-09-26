from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum
from .models import Product, Movement


def recalculate_stock(product: Product):
    """Recalcule le stock actuel du produit en fonction des mouvements."""
    total_in = product.movements.filter(movement_type='IN').aggregate(
        s=Sum('quantity'))['s'] or 0
    total_out = product.movements.filter(movement_type='OUT').aggregate(
        s=Sum('quantity'))['s'] or 0

    product.current_stock = product.quantity + total_in - total_out
    product.save(update_fields=['current_stock'])


@receiver(post_save, sender=Movement)
def update_stock_on_save(sender, instance, **kwargs):
    product = instance.product
    product.last_stock = product.current_stock
    product.save(update_fields=['last_stock'])
    recalculate_stock(product)


@receiver(post_delete, sender=Movement)
def update_stock_on_delete(sender, instance, **kwargs):
    product = instance.product
    product.last_stock = product.current_stock
    product.save(update_fields=['last_stock'])
    recalculate_stock(product)




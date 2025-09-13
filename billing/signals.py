# billing/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import InvoiceItem
from stock.models import Product

@receiver(post_save, sender=InvoiceItem)
def update_stock_after_invoiceitem(sender, instance, created, **kwargs):
    """Décrémente le stock après ajout d’un produit dans une facture."""
    if created:  # seulement à la création
        product = instance.product
        if product.quantity >= instance.quantity:
            product.quantity -= instance.quantity
        else:
            # sécurité : si le stock est insuffisant, on peut le mettre à 0
            product.quantity = 0
        product.save()

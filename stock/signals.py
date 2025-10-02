from django.db.models import Sum
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Product, Movement,Category
from django.db.models.signals import post_migrate


@receiver(post_save, sender=Product)
def init_current_stock(sender, instance, created, **kwargs):
    """
    Lors de la création d'un produit, initialise le stock actuel et last_stock
    à la quantité initiale définie dans le champ quantity.
    """
    if created:
        # Si current_stock ou last_stock ne sont pas encore définis
        if instance.current_stock is None or instance.current_stock == 0:
            instance.current_stock = instance.quantity
        if instance.last_stock is None or instance.last_stock == 0:
            instance.last_stock = instance.quantity
        instance.save(update_fields=['current_stock', 'last_stock'])


def apply_movement(product: Product, movement_type: str, movement_quantity: int):
    """
    Applique un mouvement sur le stock actuel.
    """
    current_stock = product.current_stock or 0
    last_stock = product.last_stock or 0
    if movement_type == 'IN':
        new_stock = last_stock+ movement_quantity
    elif movement_type == 'OUT':
        new_stock = last_stock - movement_quantity
        if new_stock < 0:
            raise ValueError("La quantité OUT dépasse le stock disponible.")
    else:
        raise ValueError("Type de mouvement inconnu")

    # mémoriser l'état avant mouvement et enregistrer
    product.last_stock = current_stock
    product.current_stock = new_stock
    product.save(update_fields=['last_stock', 'current_stock'])


def recompute_current_stock(product: Product):
    """
    Recalcule complètement le stock actuel à partir du stock initial + tous les mouvements.
    """
    total_in = product.movements.filter(movement_type='IN').aggregate(
        s=Sum('movement_quantity')
    )['s'] or 0
    total_out = product.movements.filter(movement_type='OUT').aggregate(
        s=Sum('movement_quantity')
    )['s'] or 0

    # quantity = stock initial défini sur Product
    product.current_stock = product.quantity + total_in - total_out
    product.save(update_fields=['current_stock'])


@receiver(post_save, sender=Movement)
def update_stock_on_save(sender, instance, created, **kwargs):
    """
    Signal : chaque fois qu'un Movement est créé ou mis à jour,
    on met à jour last_stock puis on applique le mouvement.
    """
    product = instance.product

    # On mémorise le stock avant le mouvement
    product.last_stock = product.current_stock
    product.save(update_fields=['last_stock'])

    # On applique ce mouvement précis
    apply_movement(product, instance.movement_type, instance.movement_quantity)


@receiver(post_delete, sender=Movement)
def update_stock_on_delete(sender, instance, **kwargs):
    """
    Signal : si un Movement est supprimé, on recalcule le stock complet.
    """
    recompute_current_stock(instance.product)

@receiver(post_migrate)
def create_default_categories(sender, **kwargs):
    """
    Crée les catégories par défaut après chaque migration.
    """
    if sender.name == 'stock':  # n’exécute que pour ton app "stock"
        defaults = [
            ('consommable', 'Consommable'),
            ('medicament', 'Médicament'),
            ('materiel', 'Matériel'),
            ('autre', 'Autre'),
        ]
        for code, label in defaults:
            Category.objects.get_or_create(name=code)
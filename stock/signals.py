from django.db.models import Sum
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Product, Movement,Category
from django.db.models.signals import post_migrate
from django.core.exceptions import ValidationError



from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum
from .models import Product, Movement, Category


@receiver(post_save, sender=Product)
def init_current_stock(sender, instance, created, **kwargs):
    """
    À la création d’un produit :
    - quantity = stock initial de référence.
    - current_stock et last_stock sont alignés sur quantity.
    """
    if created:
        instance.current_stock = instance.quantity
        instance.last_stock = instance.quantity
        instance.save(update_fields=['current_stock', 'last_stock'])


def apply_movement(product: Product, movement: Movement):
    """
    Applique un mouvement unique sur un produit.
    Le mouvement contient :
      - movement_type : 'IN' ou 'OUT'
      - movement_quantity : quantité du mouvement
    """

    # 1️⃣ Stock avant mouvement
    stock_avant = product.last_stock

    # 2️⃣ Calcul du stock après mouvement
    if movement.movement_type == 'IN':
        stock_apres = stock_avant + movement.movement_quantity
    elif movement.movement_type == 'OUT':
        if movement.movement_quantity > stock_avant:
            raise ValueError("La quantité OUT dépasse le stock disponible.")
        stock_apres = stock_avant - movement.movement_quantity
    else:
        raise ValueError("Type de mouvement inconnu.")

    # 3️⃣ Mise à jour du mouvement (trace exacte)
    movement.last_stock = stock_avant
    movement.save(update_fields=['last_stock'])

    # 4️⃣ Mise à jour du produit
    product.last_stock = stock_avant
    product.current_stock = stock_apres
    product.save(update_fields=['last_stock', 'current_stock'])


@receiver(post_save, sender=Movement)
def update_stock_on_movement(sender, instance, created, **kwargs):
    if not created:
        return

    product = instance.product

    # Sauvegarder l'ancien stock avant le mouvement
    stock_avant = product.current_stock or 0
    product.last_stock = stock_avant

    # Calcul du nouveau stock selon le type
    if instance.movement_type == 'IN':
        stock_apres = stock_avant + instance.movement_quantity
    elif instance.movement_type == 'OUT':
        if instance.movement_quantity > stock_avant:
            raise ValidationError(
                f"Stock insuffisant pour le produit {product.name}. "
                f"Disponible : {stock_avant}, demandé : {instance.movement_quantity}."
            )
        stock_apres = stock_avant - instance.movement_quantity

    else:
        raise ValidationError("Type de mouvement inconnu.")

    product.current_stock = stock_apres
    product.save(update_fields=['last_stock', 'current_stock'])


def recompute_current_stock(product: Product):
    """
    Recalcule le stock complet à partir du stock initial et de tous les mouvements.
    """
    total_in = product.movements.filter(movement_type='IN').aggregate(s=Sum('movement_quantity'))['s'] or 0
    total_out = product.movements.filter(movement_type='OUT').aggregate(s=Sum('movement_quantity'))['s'] or 0

    product.current_stock = product.quantity + total_in - total_out
    product.last_stock = product.current_stock
    product.save(update_fields=['current_stock', 'last_stock'])


@receiver(post_delete, sender=Movement)
def update_stock_on_delete(sender, instance, **kwargs):
    """
    Lorsqu’un mouvement est supprimé, on recalcule complètement le stock du produit.
    """
    recompute_current_stock(instance.product)


@receiver(post_migrate)
def create_default_categories(sender, **kwargs):
    """
    Crée les catégories par défaut après chaque migration.
    """
    if sender.name == 'stock':
        defaults = [
            ('consommable', 'Consommable'),
            ('medicament', 'Médicament'),
            ('materiel', 'Matériel'),
            ('autre', 'Autre'),
        ]
        for code, label in defaults:
            Category.objects.get_or_create(name=code)

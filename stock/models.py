# stock/models.py
from django.db import models
from datetime import date 
from django.db import models
from django.db.models import Sum
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver



class Category(models.Model):
    CATEGORY_CHOICES = [
        ('consommable', 'Consommable'),
        ('medicament', 'Médicament'),
        ('materiel', 'Matériel'),
        ('autre', 'Autre'),
    ]
    name = models.CharField(max_length=100, choices=CATEGORY_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()




class Product(models.Model):
    
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True,)
    quantity = models.PositiveIntegerField(default=0)  # stock initial
    last_stock = models.IntegerField(default=0)  # stock avant dernier mouvement
    current_stock = models.IntegerField(default=0)  # stock actuel recalculé
    description = models.TextField(blank=True)
    expiration_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Movement(models.Model):
    MOVEMENT_CHOICES = [
        ('IN', 'Entrée'),
        ('OUT', 'Sortie')
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='movements')
    movement_type = models.CharField(max_length=3, choices=MOVEMENT_CHOICES)
    movement_quantity = models.PositiveIntegerField()
    last_stock = models.IntegerField(default=0)  # stock avant ce mouvement
    note = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_movement_type_display()} - {self.product.name} ({self.quantity})"



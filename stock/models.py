# stock/models.py
from django.db import models
from datetime import date

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
    quantity = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)
    expiration_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def current_stock(self):
        # Calculer le stock en fonction des mouvements
        stock_in = sum(m.quantity for m in self.movements.filter(movement_type='IN'))
        stock_out = sum(m.quantity for m in self.movements.filter(movement_type='OUT'))
        return self.quantity + stock_in - stock_out

    def __str__(self):
        return self.name

class Movement(models.Model):
    MOVEMENT_CHOICES = [
        ('IN', 'Entrée'),
        ('OUT', 'Sortie')
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='movements')
    movement_type = models.CharField(max_length=3, choices=MOVEMENT_CHOICES)
    quantity = models.PositiveIntegerField()
    note = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_movement_type_display()} - {self.product.name} ({self.quantity})"

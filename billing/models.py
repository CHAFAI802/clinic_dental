from django.db import models
from patients.models import Patient
from stock.models import Product
class Invoice(models.Model):
    patient = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[("unpaid", "Non payé"), ("paid", "Payé"), ("partial", "Partiel")],
        default="unpaid"
    )

    def __str__(self):
        return f"Facture #{self.id} - {self.patient}"

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Payment(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="payments")
    date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(
        max_length=20,
        choices=[("cash", "Espèces"), ("card", "Carte bancaire"), ("transfer", "Virement")]
    )

    def __str__(self):
        return f"Paiement {self.amount}€ pour Facture #{self.invoice.id}"

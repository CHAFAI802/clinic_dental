# stock/forms.py
from django import forms
from .models import Product, Movement,Category
from datetime import date

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'quantity', 'description', 'expiration_date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}), 
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'expiration_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def clean_expiration_date(self):
        exp_date = self.cleaned_data.get('expiration_date')
        if exp_date and exp_date < date.today():
            raise forms.ValidationError("La date d'expiration ne peut pas être dans le passé.")
        return exp_date

class MovementForm(forms.ModelForm):
    class Meta:
        model = Movement
        fields = ['product', 'movement_type', 'movement_quantity', 'note']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-select'}),
            'movement_type': forms.Select(attrs={'class': 'form-select'}),
            'movement_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def clean_movement_quantity(self):
        movement_quantity = self.cleaned_data.get('movement_quantity')
        product = self.cleaned_data.get('product')
        movement_type = self.cleaned_data.get('movement_type')

        # Si c’est une sortie, on vérifie le stock actuel
        if movement_type == 'OUT' and product:
            # suppose que ton modèle Product a un champ "quantity" = stock actuel
            if movement_quantity > product.current_stock:
                raise forms.ValidationError(
                    f"La quantité demandée ({movement_quantity}) dépasse le stock actuel du produit "
                    f"({product.current_stock})."
                )

        return movement_quantity
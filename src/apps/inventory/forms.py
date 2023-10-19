from django import forms

from src.apps.inventory.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "category", "price", "is_active", "stock"]

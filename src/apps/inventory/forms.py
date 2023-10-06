from django import forms

from src.apps.inventory.models import Product, Category


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "category", "price"]


class ProductFilterForm(forms.Form):
    name = forms.CharField(label="Product Name", required=False)
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), empty_label="Select Category", required=False
    )
    min_price = forms.DecimalField(label="Minimum Price", required=False)
    max_price = forms.DecimalField(label="Maximum Price", required=False)
    order_by = forms.ChoiceField(
        label="Order by",
        choices=[
            ("", "None"),
            ("name", "Name (A-Z)"),
            ("-name", "Name (Z-A)"),
            ("price", "Price (Low to High)"),
            ("-price", "Price (High to Low)"),
        ],
        required=False,
    )

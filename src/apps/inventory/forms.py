from django import forms

from src.apps.inventory.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "category", "price"]


# class ProductFilterForm(forms.Form):
#     name = forms.CharField(label="Product Name", required=False)
#     category = forms.ModelChoiceField(
#         queryset=Category.objects.all(), empty_label="Select Category", required=False
#     )
#     min_price = forms.DecimalField(label="Minimum Price", required=False)
#     max_price = forms.DecimalField(label="Maximum Price", required=False)

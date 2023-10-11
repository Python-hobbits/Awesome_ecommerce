from django import forms

from .models import DeliveryOption


class DeliveryOptionForm(forms.ModelForm):
    class Meta:
        model = DeliveryOption
        fields = ["delivery_method", "shipment_address"]
        widgets = {
            "delivery_method": forms.RadioSelect,
            "shipment_address": forms.Textarea(attrs={"rows": 3}),
        }

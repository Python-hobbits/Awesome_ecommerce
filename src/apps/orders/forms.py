from django import forms

from src.apps.orders.models import DeliveryOption, PaymentMethod


class DeliveryOptionForm(forms.ModelForm):
    class Meta:
        model = DeliveryOption
        fields = ["delivery_method", "shipment_address"]
        widgets = {
            "delivery_method": forms.RadioSelect,
            "shipment_address": forms.Textarea(attrs={"rows": 3}),
        }

        error_messages = {
            "delivery_method": {
                "required": "Delivery method is required.",
            },
        }

    def clean(self):
        cleaned_data = super().clean()
        delivery_method = cleaned_data.get("delivery_method")
        shipment_address = cleaned_data.get("shipment_address")

        if delivery_method == "delivery" and not shipment_address:
            self.add_error(
                "shipment_address",
                'Shipment address is required when delivery method is "Delivery".',
            )
        return cleaned_data


class PaymentMethodForm(forms.ModelForm):
    class Meta:
        model = PaymentMethod
        fields = ["payment_method"]
        widgets = {"payment_method": forms.RadioSelect}

        error_messages = {
            "payment_method": {
                "required": "Payment method is required.",
            },
        }

from decimal import Decimal

from django.conf import settings
from django.db import models

from src.apps.inventory.models import Product


class Order(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=255)
    user_email = models.EmailField()

    def __str__(self):
        return f"Order ID {self.id}"


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.PROTECT)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()

    def __str__(self):
        return f"Product {self.product_id} in Order {self.order_id}"

    def get_total_price(self):
        return self.product_price * Decimal(self.quantity)


class DeliveryOption(models.Model):
    DELIVERY_CHOICES = [
        ("delivery", "Delivery"),
        ("pickup", "Pickup"),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    delivery_method = models.CharField(max_length=10, choices=DELIVERY_CHOICES)
    shipment_address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.delivery_method


class PaymentMethod(models.Model):
    PAYMENT_CHOICES = [
        ("credit_card", "Credit Card"),
        ("bank_transfer", "Bank transfer"),
        ("cash", "Cash payment on delivery"),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=30, choices=PAYMENT_CHOICES)

    def __str__(self):
        return self.payment_method

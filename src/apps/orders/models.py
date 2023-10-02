from django.db import models

from src.apps.inventory.models import Product


class Order(models.Model):
    user_id = models.IntegerField()
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

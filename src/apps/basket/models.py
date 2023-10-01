from django.db import models

from src.apps.inventory.models import Product
from src.apps.user.models import User


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"Basket for {self.user.username}: {self.quantity} x {self.product.name}"

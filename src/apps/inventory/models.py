from django.db import models

from src.apps.user.models import User


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="products",
        limit_choices_to={"user_type": "Seller"},
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

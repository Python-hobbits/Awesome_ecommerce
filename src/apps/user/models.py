from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class UserType(models.TextChoices):
        CUSTOMER = "Customer"
        SELLER = "Seller"
        ADMIN = "Admin"

    user_type = models.CharField(
        verbose_name="User type",
        max_length=32,
        choices=UserType.choices,
        default=UserType.ADMIN,
    )

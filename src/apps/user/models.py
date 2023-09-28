from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class UserType(models.Choices):
        CUSTOMER = "Customer"
        SELLER = "Seller"
        ADMIN = "Admin"

    user_type = models.CharField(
        verbose_name="User type",
        max_length=32,
        choices=UserType.choices,
        default=UserType.ADMIN,
    )

    user_profile = models.OneToOneField(
        verbose_name="User type",
        to="user.UserProfile",
        related_name="users",
        on_delete=models.SET_NULL,
        null=True,
    )

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class UserProfile(models.Model):
    pass

    class Meta:
        verbose_name = "User profile"
        verbose_name_plural = "User profiles"

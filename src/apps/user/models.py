from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    user_profile = models.ForeignKey(
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
    title = models.CharField(
        verbose_name="Title",
        max_length=32,
        blank=False,
        null=False,
    )

    class Meta:
        verbose_name = "User profile"
        verbose_name_plural = "User profiles"

    def __str__(self):
        return f"{self.title}"

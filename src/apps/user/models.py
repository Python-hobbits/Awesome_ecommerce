import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


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

    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, verbose_name="User UUID"
    )

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    user_profile = models.OneToOneField(
        "UserProfile",
        on_delete=models.SET_NULL,
        null=True,
    )


class UserProfile(models.Model):
    profile_picture = models.ImageField(upload_to="profile_pictures/", blank=True, null=True)
    address = models.OneToOneField("UserAddress", on_delete=models.SET_NULL, blank=True, null=True)
    mobile_phone = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        verbose_name = "User profile"
        verbose_name_plural = "User profiles"


class UserAddress(models.Model):
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    building = models.CharField(max_length=10)
    apartment = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.street}, {self.building}, {self.apartment}, {self.city}, {self.country}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

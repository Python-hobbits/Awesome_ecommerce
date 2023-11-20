import uuid

from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from src.config.storage_backends import get_storage, StorageType


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
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name="User UUID",
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
    @staticmethod
    def profile_picture_path(instance, filename):
        # Generate a UUID and use it as part of the filename
        ext = filename.split(".")[-1]
        filename = f"{uuid.uuid4()}.{ext}"
        return f"profile_pictures/{filename}"

    profile_picture = models.ImageField(
        upload_to=profile_picture_path,
        storage=get_storage(StorageType.PRIVATE),
        blank=True,
        null=True,
        validators=[FileExtensionValidator(["jpg", "jpeg", "png"])],
    )
    address = models.OneToOneField("UserAddress", on_delete=models.SET_NULL, blank=True, null=True)
    mobile_phone = models.CharField(max_length=15, blank=True, null=True)


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

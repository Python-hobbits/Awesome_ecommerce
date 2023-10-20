from autoslug import AutoSlugField
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    slug = AutoSlugField(populate_from="name", unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, self.id)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("category_detail", args=[str(self.slug)])


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="products",
        limit_choices_to={"user_type": "Seller"},
    )
    created_at = models.DateTimeField(auto_now_add=True)
    slug = AutoSlugField(populate_from="name", unique=True)
    is_active = models.BooleanField(default=True)
    stock = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, self.id)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("product_detail", args=[str(self.category.slug), str(self.slug)])

    def active_images(self):
        return self.images.filter(is_active=True)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="product_images/")
    is_active = models.BooleanField(default=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    deactivated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Image for {self.product.name} ({'Active' if self.is_active else 'Inactive'})"

from autoslug.utils import slugify
from django.conf import settings
from django.db import models
from django.urls import reverse

STATUS = ((0, "Draft"), (1, "Publish"))


class Page(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="page"
    )
    description = models.CharField(max_length=255)
    context = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.CharField(max_length=255, blank=True)
    canonical_path = models.CharField(max_length=255, default="", blank=True)
    robots_index = models.BooleanField(default=True)
    robots_follow = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_on"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        if not self.meta_title:
            self.meta_title = self.title

        if not self.meta_description:
            self.meta_description = self.description

        if not self.canonical_path:
            self.canonical_path = reverse("page", kwargs={"page_slug": self.slug})

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

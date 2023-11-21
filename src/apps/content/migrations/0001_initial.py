# Generated by Django 4.2.5 on 2023-11-21 14:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Page",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("title", models.CharField(max_length=255, unique=True)),
                ("slug", models.SlugField(blank=True, max_length=255, unique=True)),
                ("description", models.CharField(max_length=255)),
                ("context", models.TextField()),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("updated_on", models.DateTimeField(auto_now=True)),
                ("status", models.IntegerField(choices=[(0, "Draft"), (1, "Publish")], default=0)),
                ("meta_title", models.CharField(blank=True, max_length=255)),
                ("meta_description", models.CharField(blank=True, max_length=255)),
                ("canonical_path", models.CharField(blank=True, default="", max_length=255)),
                ("robots_index", models.BooleanField(default=True)),
                ("robots_follow", models.BooleanField(default=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="page",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-created_on"],
            },
        ),
    ]
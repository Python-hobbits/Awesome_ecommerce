# Generated by Django 4.2.5 on 2023-10-25 13:22

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0005_fill_user_uuid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="user_type",
            field=models.CharField(
                choices=[("Customer", "Customer"), ("Seller", "Seller"), ("Admin", "Admin")],
                default="Admin",
                max_length=32,
                verbose_name="User type",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="uuid",
            field=models.UUIDField(
                default=uuid.uuid4, editable=False, unique=True, verbose_name="User UUID"
            ),
        ),
    ]
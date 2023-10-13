# Generated by Django 4.2.5 on 2023-10-13 09:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0002_alter_order_user_id_deliveryoption"),
    ]

    operations = [
        migrations.CreateModel(
            name="PaymentMethod",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "payment_method",
                    models.CharField(
                        choices=[
                            ("credit_card", "Credit Card"),
                            ("bank_transfer", "Bank transfer"),
                            ("cash", "Cash payment on delivery"),
                        ],
                        max_length=30,
                    ),
                ),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="orders.order"
                    ),
                ),
            ],
        ),
    ]
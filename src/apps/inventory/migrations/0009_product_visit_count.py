# Generated by Django 4.2.5 on 2023-10-20 09:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("inventory", "0008_productimage"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="visit_count",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
# Generated by Django 4.2.5 on 2023-10-03 10:34

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("inventory", "0003_product_created_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="slug",
            field=autoslug.fields.AutoSlugField(
                default="", editable=False, populate_from="name"
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="product",
            name="slug",
            field=autoslug.fields.AutoSlugField(
                default="", editable=False, populate_from="name"
            ),
            preserve_default=False,
        ),
    ]

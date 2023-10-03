# Generated by Django 4.2.5 on 2023-10-03 09:02

from django.db import migrations, models


def populate_slug_with_id(apps, schema_editor):
    Product = apps.get_model('inventory', 'Product')
    Category = apps.get_model('inventory', 'Category')

    for product in Product.objects.all():
        product.slug = f'product_{product.id}'
        product.save()

    for category in Category.objects.all():
        category.slug = f'category_{category.id}'
        category.save()

def reverse_populate_slug_with_id(apps, schema_editor):
    Product = apps.get_model('inventory', 'Product')
    Category = apps.get_model('inventory', 'Category')

    # Reverse the population of the slug field for Product
    for product in Product.objects.all():
        product.slug = ''
        product.save()

    # Reverse the population of the slug field for Category
    for category in Category.objects.all():
        category.slug = ''
        category.save()

class Migration(migrations.Migration):
    dependencies = [
        ("inventory", "0004_category_slug_product_slug"),
    ]

    operations = [
        migrations.RunPython(populate_slug_with_id, reverse_code=reverse_populate_slug_with_id),

        migrations.AlterField(
            model_name="category",
            name="slug",
            field=models.SlugField(unique=True),
        ),
        migrations.AlterField(
            model_name="product",
            name="slug",
            field=models.SlugField(unique=True),
        ),
    ]

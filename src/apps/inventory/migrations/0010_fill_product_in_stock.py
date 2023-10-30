from django.db import migrations


def set_in_stock(apps, schema_editor):
    Product = apps.get_model('inventory', 'Product')
    for product in Product.objects.all():
        product.in_stock = product.stock > 0
        product.save()


class Migration(migrations.Migration):
    dependencies = [
        ("inventory", "0009_product_in_stock"),
    ]

    operations = [
        migrations.RunPython(set_in_stock),
    ]

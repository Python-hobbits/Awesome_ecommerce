from django.contrib import admin

from src.apps.inventory.models import Category, Product

admin.site.register(Category)
admin.site.register(Product)

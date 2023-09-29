from django.views.generic import DetailView

from src.apps.inventory.models import Product


class ProductDetailView(DetailView):
    model = Product

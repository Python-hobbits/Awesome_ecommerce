from django_redis import get_redis_connection

from src.apps.inventory.models import Product


class MostViewedProductsMixin:
    def get_most_viewed_products(self):
        r = get_redis_connection("default")
        most_viewed_products_ids = r.zrevrange("product-views", 0, 2)
        most_viewed_products = [
            Product.objects.get(id=int(product_id)) for product_id in most_viewed_products_ids
        ]
        return most_viewed_products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["most_viewed_products"] = self.get_most_viewed_products()
        return context

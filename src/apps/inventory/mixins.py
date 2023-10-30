from collections import OrderedDict

from django_redis import get_redis_connection

from src.apps.inventory.models import Product


class MostViewedProductsMixin:
    def get_most_viewed_products(self):
        redis = get_redis_connection("redis_cache")
        most_viewed_products_ids = redis.zrevrange("product-views", 0, 2)

        products = Product.objects.in_bulk(map(int, most_viewed_products_ids))
        ordered_products = OrderedDict(
            (int(product_id), products[int(product_id)]) for product_id in most_viewed_products_ids
        )
        most_viewed_products = list(ordered_products.values())

        return most_viewed_products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["most_viewed_products"] = self.get_most_viewed_products()
        return context

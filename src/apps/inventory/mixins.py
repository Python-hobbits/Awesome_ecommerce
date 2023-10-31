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


class LastViewedProductsMixin:
    def get_last_viewed_products(self):
        redis = get_redis_connection("redis_cache")
        user = self.request.user
        if user.is_authenticated:
            user_key = f"user:{user.uuid}:recentviews"
        else:
            user_key = f"session:{self.request.session.session_key}:recentviews"

        last_viewed_products_ids = redis.zrevrange(user_key, 0, 2)
        products = Product.objects.in_bulk(map(int, last_viewed_products_ids))
        ordered_products = OrderedDict(
            (int(product_id), products[int(product_id)]) for product_id in last_viewed_products_ids
        )
        last_viewed_products = list(ordered_products.values())

        return last_viewed_products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["last_viewed_products"] = self.get_last_viewed_products()
        return context


class ProductViewsCounterMixin:
    def get(self, request, *args, **kwargs):
        product = self.get_object()
        redis = get_redis_connection("redis_cache")
        redis.zincrby("product-views", 1, product.id)

        return super().get(request, *args, **kwargs)


class LastViewedProductsCounterMixin:
    def get(self, request, *args, **kwargs):
        product = self.get_object()
        user = self.request.user

        if user.is_authenticated:
            user_key = f"user:{user.uuid}:recentviews"
        else:
            user_key = f"session:{request.session.session_key}:recentviews"

        redis = get_redis_connection("redis_cache")

        view_count = redis.incr(f"{user_key}:counter")
        redis.zadd(user_key, {product.id: view_count})

        return super().get(request, *args, **kwargs)

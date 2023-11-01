from collections import OrderedDict
from time import time

from django_redis import get_redis_connection

from src.apps.inventory.models import Product
from src.config import settings


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

        # each GET request will increment the product view counter by 1
        redis.zincrby("product-views", 1, product.id)

        return super().get(request, *args, **kwargs)


class LastViewedProductsCounterMixin:
    def get(self, request, *args, **kwargs):
        product = self.get_object()
        user = self.request.user

        user_key = None

        if user.is_authenticated:
            user_key = f"user:{user.uuid}:recentviews"
        elif request.session.session_key is not None:
            user_key = f"session:{request.session.session_key}:recentviews"

        if user_key:
            redis = get_redis_connection("redis_cache")

            # add products to sorted set with time in seconds as a score
            redis.zadd(user_key, {product.id: time()})

            # keep only 10 last viewed products in table
            num_last_viewed_products = 10
            redis.zremrangebyrank(user_key, 0, -num_last_viewed_products - 1)

            # delete key once session in over
            redis.expire(user_key, settings.SESSION_COOKIE_AGE)

        return super().get(request, *args, **kwargs)

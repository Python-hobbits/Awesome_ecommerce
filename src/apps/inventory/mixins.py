from time import time

from django.conf import settings
from django_redis import get_redis_connection

from src.apps.inventory.models import Product


class RedisConnectionMixin:
    def get_redis_connection(self, db="redis_cache"):
        return get_redis_connection(db)


class MostViewedProductsMixin(RedisConnectionMixin):
    most_viewed_products_to_show = None

    def get_most_viewed_products(self):
        if not settings.CACHES_ENABLE:
            return []
        redis = self.get_redis_connection()

        most_viewed_products_to_show = self.most_viewed_products_to_show
        if not most_viewed_products_to_show:
            most_viewed_products_to_show = settings.DEFAULT_MOST_VIEWED_PRODUCTS_TO_SHOW

        most_viewed_products_ids = redis.zrevrange("product-views", 0, most_viewed_products_to_show)
        products = Product.objects.in_bulk(most_viewed_products_ids)
        most_viewed_products = [
            products[int(product_id)]
            for product_id in most_viewed_products_ids
            if int(product_id) in products
        ]

        return most_viewed_products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["most_viewed_products"] = self.get_most_viewed_products()
        return context


class LastViewedProductsMixin(RedisConnectionMixin):
    last_viewed_products_to_show = None

    def get_last_viewed_products(self):
        if not settings.CACHES_ENABLE:
            return []
        redis = self.get_redis_connection()
        user = self.request.user
        if user.is_authenticated:
            user_key = f"user:{user.uuid}:recentviews"
        else:
            user_key = f"session:{self.request.session.session_key}:recentviews"

        last_viewed_products_to_show = self.last_viewed_products_to_show
        if not last_viewed_products_to_show:
            last_viewed_products_to_show = settings.DEFAULT_LAST_VIEWED_PRODUCTS_TO_SHOW

        last_viewed_products_ids = redis.zrevrange(user_key, 0, last_viewed_products_to_show - 1)
        products = Product.objects.in_bulk(last_viewed_products_ids)
        last_viewed_products = [
            products[int(product_id)]
            for product_id in last_viewed_products_ids
            if int(product_id) in products
        ]

        return last_viewed_products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["last_viewed_products"] = self.get_last_viewed_products()
        return context


class ProductViewsCounterMixin(RedisConnectionMixin):
    def get(self, request, *args, **kwargs):
        if not settings.CACHES_ENABLE:
            return super().get(request, *args, **kwargs)
        product = self.get_object()
        redis = self.get_redis_connection()

        # each GET request will increment the product view counter by 1
        redis.zincrby("product-views", 1, product.id)

        return super().get(request, *args, **kwargs)


class LastViewedProductsCounterMixin(RedisConnectionMixin):
    def get(self, request, *args, **kwargs):
        if not settings.CACHES_ENABLE:
            return super().get(request, *args, **kwargs)
        product = self.get_object()
        user = self.request.user

        user_key = None

        if user.is_authenticated:
            user_key = f"user:{user.uuid}:recentviews"
        elif request.session.session_key is not None:
            user_key = f"session:{request.session.session_key}:recentviews"

        if user_key:
            redis = self.get_redis_connection()

            # add products to sorted set with time in seconds as a score
            redis.zadd(user_key, {product.id: time()})

            # keep only 10 last viewed products in table
            redis.zremrangebyrank(user_key, 0, -settings.LAST_VIEWED_PRODUCTS_TO_KEEP - 1)

            # delete key once session in over
            redis.expire(user_key, settings.SESSION_COOKIE_AGE)

        return super().get(request, *args, **kwargs)

import json

from django.db.models import Case, When
from django.views.generic import TemplateView

from src.apps.inventory.models import Product
from src.apps.inventory.redis_utils import RedisConnection


class IndexView(TemplateView):
    template_name = "content/index.html"

    def get_product_views(self):
        redis_conn = RedisConnection()
        redis_connection = redis_conn.get_connection()

        product_views_data = redis_connection.get("product:views")

        if product_views_data:
            product_views = json.loads(product_views_data)

            sorted_product_views = sorted(product_views.items(), key=lambda x: x[1], reverse=True)
            sorted_ids = [id[0] for id in sorted_product_views][:3]
            print(f"Sorted ids {sorted_ids}")

            products = Product.objects.filter(id__in=sorted_ids).order_by(
                Case(*[When(id=id, then=pos) for pos, id in enumerate(sorted_ids)])
            )

            return products

        return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = self.get_product_views()
        return context


class AboutUsView(TemplateView):
    template_name = "support/about_us.html"


class DeliveryView(TemplateView):
    template_name = "support/delivery.html"


class TermsAndConditionsView(TemplateView):
    template_name = "support/terms_and_conditions.html"

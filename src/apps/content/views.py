from django.views.generic import TemplateView, DetailView

from src.apps.content.models import Page
from src.apps.inventory.mixins import MostViewedProductsMixin, LastViewedProductsMixin


class IndexView(MostViewedProductsMixin, LastViewedProductsMixin, TemplateView):
    template_name = "content/index.html"


class AboutUsView(TemplateView):
    template_name = "support/about_us.html"


class DeliveryView(TemplateView):
    template_name = "support/delivery.html"


class TermsAndConditionsView(TemplateView):
    template_name = "support/terms_and_conditions.html"


class PageView(DetailView):
    model = Page
    template_name = "content/page.html"
    context_object_name = "page"
    slug_url_kwarg = "page_slug"

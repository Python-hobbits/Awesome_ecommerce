from django.views.generic import TemplateView

from src.apps.inventory.mixins import MostViewedProductsMixin


class IndexView(MostViewedProductsMixin, TemplateView):
    template_name = "content/index.html"


class AboutUsView(TemplateView):
    template_name = "support/about_us.html"


class DeliveryView(TemplateView):
    template_name = "support/delivery.html"


class TermsAndConditionsView(TemplateView):
    template_name = "support/terms_and_conditions.html"

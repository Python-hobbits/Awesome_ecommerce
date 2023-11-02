from django.views.generic import TemplateView

from src.apps.inventory.mixins import MostViewedProductsMixin, LastViewedProductsMixin


class IndexView(MostViewedProductsMixin, LastViewedProductsMixin, TemplateView):
    template_name = "content/index.html"


class AboutUsView(TemplateView):
    template_name = "support/about_us.html"


class DeliveryView(TemplateView):
    template_name = "support/delivery.html"


class TermsAndConditionsView(TemplateView):
    template_name = "support/terms_and_conditions.html"

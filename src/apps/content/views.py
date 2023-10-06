from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "content/index.html"


class AboutUsView(TemplateView):
    template_name = "support/about_us.html"


class DeliveryView(TemplateView):
    template_name = "support/delivery.html"

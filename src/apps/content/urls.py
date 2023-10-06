from django.urls import path

from src.apps.content.views import IndexView, AboutUsView, DeliveryView, TermsAndConditionsView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("about_us", AboutUsView.as_view(), name="about_us"),
    path("delivery", DeliveryView.as_view(), name="delivery"),
    path("terms", TermsAndConditionsView.as_view(), name="terms_and_conditions"),
]

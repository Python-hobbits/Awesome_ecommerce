from django.urls import path

from src.apps.content.views import IndexView, AboutUsView, DeliveryView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("about_us", AboutUsView.as_view(), name="about_us"),
    path("delivery", DeliveryView.as_view(), name="delivery"),
]

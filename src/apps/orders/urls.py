from django.urls import path

from src.apps.orders.views import CheckoutView

urlpatterns = [
    path("", CheckoutView.as_view(), name="checkout"),
]

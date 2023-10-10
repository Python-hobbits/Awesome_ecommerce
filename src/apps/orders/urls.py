from django.urls import path

from src.apps.orders import views
from src.apps.orders.views import CheckoutView

urlpatterns = [
    path("", CheckoutView.as_view(), name="checkout"),
    path("thank_you/<int:order_id>/", views.thank_you_view, name="thank_you")
]

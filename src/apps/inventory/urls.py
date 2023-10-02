from django.urls import path

from src.apps.inventory.views import ProductDetailView, ProductBySellerListView

urlpatterns = [
    path("<pk>/", ProductDetailView.as_view()),
    path("seller/my_products", ProductBySellerListView.as_view()),
]

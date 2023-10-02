from django.urls import path

from src.apps.inventory.views import ProductBySellerListView, ProductDetailView

urlpatterns = [
    path("<pk>/", ProductDetailView.as_view()),
    path("seller/my_products", ProductBySellerListView.as_view()),
]

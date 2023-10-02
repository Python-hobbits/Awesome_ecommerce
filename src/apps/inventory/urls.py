from django.urls import path

from src.apps.inventory.views import (
    ProductDetailView,
    ProductBySellerListView,
    CategoryDetailView,
    ProductListView,
)

urlpatterns = [
    path("seller/my_products", ProductBySellerListView.as_view(), name="product_by_seller"),
    path("category/<slug:category_slug>/", CategoryDetailView.as_view(), name="category_detail"),
    path(
        "<slug:category_slug>/<slug:product_slug>/",
        ProductDetailView.as_view(),
        name="product_detail",
    ),
    path("", ProductListView.as_view(), name="product_list"),
]

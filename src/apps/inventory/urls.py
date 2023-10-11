from django.urls import path

from src.apps.inventory.views import (
    ProductDetailView,
    ProductBySellerListView,
    CategoryDetailView,
    ProductListView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
)

urlpatterns = [
    path("seller/my_products", ProductBySellerListView.as_view(), name="product_by_seller"),
    path("category/<slug:category_slug>/", CategoryDetailView.as_view(), name="category_detail"),
    path(
        "product/<slug:category_slug>/<slug:product_slug>/",
        ProductDetailView.as_view(),
        name="product_detail",
    ),
    path("", ProductListView.as_view(), name="product_list"),
    path("seller/create_product/", ProductCreateView.as_view(), name="product_create"),
    path(
        "seller/edit/<slug:category_slug>/<slug:product_slug>/",
        ProductUpdateView.as_view(),
        name="product_edit",
    ),
    path(
        "seller/delete/<slug:category_slug>/<slug:product_slug>/",
        ProductDeleteView.as_view(),
        name="product_delete",
    ),
]

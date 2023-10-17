from django.urls import path

from src.apps.inventory.views import (
    ProductDetailView,
    ProductBySellerListView,
    CategoryDetailView,
    ProductListView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    DeactivatedProductBySellerListView,
)

urlpatterns = [
    path("products/my/", ProductBySellerListView.as_view(), name="product_by_seller"),
    path(
        "products/my/not_active",
        DeactivatedProductBySellerListView.as_view(),
        name="not_active_product_by_seller",
    ),
    path("category/<slug:category_slug>/", CategoryDetailView.as_view(), name="category_detail"),
    path(
        "product/<slug:category_slug>/<slug:product_slug>/",
        ProductDetailView.as_view(),
        name="product_detail",
    ),
    path("products/", ProductListView.as_view(), name="product_list"),
    path("create/", ProductCreateView.as_view(), name="product_create"),
    path(
        "<slug:category_slug>/<slug:product_slug>/edit/",
        ProductUpdateView.as_view(),
        name="product_edit",
    ),
    path(
        "<slug:category_slug>/<slug:product_slug>/delete/",
        ProductDeleteView.as_view(),
        name="product_delete",
    ),
]

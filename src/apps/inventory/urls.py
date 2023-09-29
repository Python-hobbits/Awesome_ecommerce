from django.urls import path

from src.apps.inventory.views import ProductDetailView

urlpatterns = [
    path("<pk>/", ProductDetailView.as_view()),
]
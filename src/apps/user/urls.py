from django.urls import include, path

from src.apps.user.views import (
    UserUpdateView,
    UserDetailView,
)

urlpatterns = [
    path("", include("allauth.urls")),
    path("<slug:uuid>", UserDetailView.as_view(), name="user_detail"),
    path("<slug:uuid>/edit", UserUpdateView.as_view(), name="user_edit"),
]

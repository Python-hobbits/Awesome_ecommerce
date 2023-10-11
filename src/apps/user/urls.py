from django.urls import include, path

from src.apps.user.views import UserUpdateView, ProfileDetailView, ProfileUpdateView

urlpatterns = [
    path("", include("allauth.urls")),
    path("profile/", ProfileDetailView.as_view(), name="user_profile"),
    path("edit/", UserUpdateView.as_view(), name="user_edit"),
    path("profile/update/", ProfileUpdateView.as_view(), name="update_profile"),
]

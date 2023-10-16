from django.urls import include, path

from src.apps.user.views import (
    UserUpdateView,
    UserDetailView,
    ProfileUpdateView,
    UserProfileDetailView,
)

urlpatterns = [
    path("", include("allauth.urls")),
    path("user/", UserDetailView.as_view(), name="user_detail"),
    path("edit/", UserUpdateView.as_view(), name="user_edit"),
    path("profile/edit/", ProfileUpdateView.as_view(), name="profile_edit"),
    path("profile/", UserProfileDetailView.as_view(), name="profile_detail"),
]

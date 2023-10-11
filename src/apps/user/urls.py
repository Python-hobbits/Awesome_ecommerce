from django.urls import include, path

from src.apps.user.views import UserUpdateView, UserDetailView, ProfileUpdateView

urlpatterns = [
    path("", include("allauth.urls")),
    path("user/", UserDetailView.as_view(), name="user_detail"),
    path("edit/", UserUpdateView.as_view(), name="user_edit"),
    path("profile/update/", ProfileUpdateView.as_view(), name="update_profile"),
]

from django.urls import include, path

from src.apps.user.views import UserProfileUpdateView, profile

urlpatterns = [
    path("", include("allauth.urls")),
    path("profile/", profile, name="user_profile"),
    path("profile/edit/", UserProfileUpdateView.as_view(), name="user_profile_edit"),
]

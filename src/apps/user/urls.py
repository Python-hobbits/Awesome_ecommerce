from django.urls import path, include

from src.apps.user.views import profile, UserProfileUpdateView

urlpatterns = [
    path("", include("allauth.urls")),
    path("profile/", profile, name="user-profile"),
    path("profile/edit/", UserProfileUpdateView.as_view(), name="user_profile_edit"),
]

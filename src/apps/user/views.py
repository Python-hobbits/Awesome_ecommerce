from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DetailView

from src.apps.user.forms import CustomUserChangeForm, UserProfileForm
from src.apps.user.models import UserProfile


class ProfileDetailView(LoginRequiredMixin, DetailView):
    template_name = "user/user_detail.html"
    form_class = CustomUserChangeForm
    success_url = reverse_lazy("user_profile")

    def get_object(self, queryset=None):
        return self.request.user


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = CustomUserChangeForm
    template_name = "user/user_edit.html"
    success_url = reverse_lazy("user_profile")

    def get_object(self, queryset=None):
        return self.request.user


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = "profile/profile_edit.html"  # Create this template
    success_url = reverse_lazy("profile")  # Redirect to the user's profile page

    def get_object(self, queryset=None):
        return UserProfile.objects.get(user=self.request.user)

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DetailView

from src.apps.user.forms import CustomUserChangeForm


class ProfileDetailView(LoginRequiredMixin, DetailView):
    template_name = "profile.html"
    form_class = CustomUserChangeForm
    success_url = reverse_lazy("user_profile")

    def get_object(self, queryset=None):
        return self.request.user


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = CustomUserChangeForm
    template_name = "user_profile_edit.html"
    success_url = reverse_lazy("user_profile")

    def get_object(self, queryset=None):
        return self.request.user

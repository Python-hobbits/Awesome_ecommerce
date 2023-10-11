from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DetailView

from src.apps.user.forms import CustomUserChangeForm, ProfileForm
from src.apps.user.models import UserProfile, UserAddress


class UserDetailView(LoginRequiredMixin, DetailView):
    template_name = "user/user_detail.html"
    form_class = CustomUserChangeForm
    success_url = reverse_lazy("user_detail")

    def get_object(self, queryset=None):
        return self.request.user


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = CustomUserChangeForm
    template_name = "user/user_edit.html"
    success_url = reverse_lazy("user_detail")

    def get_object(self, queryset=None):
        return self.request.user


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = ProfileForm
    template_name = "profile/profile_edit.html"
    success_url = reverse_lazy("profile_detail")

    def get_object(self, queryset=None):
        # Check if the user has a profile; if not, create one
        user = self.request.user
        UserProfile.objects.get_or_create(user=user)
        profile = UserProfile.objects.get(user=user)
        if not profile.address:
            address = UserAddress()
            address.save()
            profile.address = address
            profile.save()

        return profile

    def form_valid(self, form):
        profile = form.save(commit=False)
        address_form = ProfileForm(self.request.POST, instance=profile.address)

        if address_form.is_valid():
            address = address_form.save()
            profile.address = address

        profile.save()
        return super().form_valid(form)


class UserProfileDetailView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = "profile/profile_detail.html"

    def get_object(self, queryset=None):
        user = self.request.user
        profile = UserProfile.objects.get(user=user)
        return profile

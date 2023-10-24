from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import UpdateView, DetailView

from src.apps.user.forms import CustomUserChangeForm, ProfileForm
from src.apps.user.models import UserProfile, UserAddress


class UserDetailView(LoginRequiredMixin, DetailView):
    template_name = "user/user_detail.html"
    form_class = CustomUserChangeForm
    model = get_user_model()
    slug_field = "uuid"
    slug_url_kwarg = "uuid"

    def get_success_url(self):
        return reverse("user_detail", args=[self.object.uuid])


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = CustomUserChangeForm
    template_name = "user/user_edit.html"
    slug_field = "uuid"
    slug_url_kwarg = "uuid"

    def get_success_url(self):
        return reverse("user_detail", args=[self.object.uuid])


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = ProfileForm
    template_name = "profile/profile_edit.html"
    success_url = reverse_lazy("profile_detail")

    def get(self, request, *args, **kwargs):
        profile = self.get_object()
        if not profile.address:
            address = UserAddress()
            address.save()
            profile.address = address
            profile.save()
        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        profile = self.request.user.user_profile
        return profile

    def form_valid(self, form):
        profile = form.save(commit=False)
        profile_form = ProfileForm(self.request.POST, instance=profile.address)

        if profile_form.is_valid():
            address = profile_form.save()
            profile.address = address

        profile.save()
        return super().form_valid(form)


class UserProfileDetailView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = "profile/profile_detail.html"

    def get_object(self, queryset=None):
        profile = self.request.user.user_profile
        return profile

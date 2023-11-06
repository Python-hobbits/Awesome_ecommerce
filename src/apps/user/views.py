from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import UpdateView, DetailView

from src.apps.user.forms import UserForm, UserAddressForm, UserProfileForm


class UserDetailView(LoginRequiredMixin, DetailView):
    template_name = "user/user_detail.html"
    model = get_user_model()
    slug_field = "uuid"
    slug_url_kwarg = "uuid"


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    template_name = "user/user_edit.html"
    form_class = UserForm
    address_form_class = UserAddressForm
    profile_form_class = UserProfileForm
    slug_field = "uuid"
    slug_url_kwarg = "uuid"

    def get_success_url(self):
        return reverse("user_detail", args=[self.object.uuid])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "form" not in context:
            context["form"] = self.form_class(instance=self.object)
        if "address_form" not in context:
            context["address_form"] = self.address_form_class(
                instance=self.object.user_profile.address
            )
        if "profile_form" not in context:
            context["profile_form"] = self.profile_form_class(instance=self.object.user_profile)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=self.object)
        address_form = self.address_form_class(
            request.POST, instance=self.object.user_profile.address
        )
        profile_form = self.profile_form_class(
            request.POST, request.FILES, instance=self.object.user_profile
        )

        if form.is_valid() and address_form.is_valid() and profile_form.is_valid():
            form.save()
            address_instance = address_form.save(commit=False)
            address_instance.save()
            profile_instance = profile_form.save(commit=False)
            profile_instance.address = address_instance
            profile_instance.save()
            return self.form_valid(form)

        return self.form_invalid(form)

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from src.apps.user.forms import CustomUserChangeForm
from src.apps.user.models import User


@login_required
def profile(request):
    return render(request, "profile.html")


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = "user_profile_edit.html"
    success_url = reverse_lazy("user-profile")

    def get_object(self, queryset=None):
        return self.request.user


# def user_edit(request):
#     """
#     Processes requests for the settings page, where users
#     can edit their profiles.
#     """
#     if request.method == 'POST':
#         postdata = request.POST.copy()
#         form = UserChangeForm(postdata)
#         if form.is_valid():
#             form.save()
#     else:
#         form = UserChangeForm()
#     return render(request, "user_profile_edit.html", context=RequestContext(request))

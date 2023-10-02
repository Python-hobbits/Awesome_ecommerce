from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm
from allauth.account.forms import SignupForm


class UserSignupForm(SignupForm):
    type = forms.ChoiceField(choices=[("Seller", "Seller"), ("Customer", "Customer")])

    def custom_signup(self, request, user):
        user.user_type = self.cleaned_data["type"]
        user.save()


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "email"]

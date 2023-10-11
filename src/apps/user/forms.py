from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm
from allauth.account.forms import SignupForm

from src.apps.user.models import UserProfile


class UserSignupForm(SignupForm):
    type = forms.ChoiceField(choices=[("Seller", "Seller"), ("Customer", "Customer")])

    def custom_signup(self, request, user):
        user.user_type = self.cleaned_data["type"]
        user.save()


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "email"]


class ProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False)
    mobile_phone = forms.CharField(max_length=15, required=False)
    country = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    street = forms.CharField(max_length=100)
    building = forms.CharField(max_length=10)
    apartment = forms.CharField(max_length=10, required=False)

    class Meta:
        model = UserProfile
        fields = [
            "profile_picture",
            "mobile_phone",
            "country",
            "city",
            "street",
            "building",
            "apartment",
        ]

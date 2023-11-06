from django import forms
from django.contrib.auth import get_user_model

from src.apps.user.models import UserProfile, UserAddress


class UserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "email"]


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["profile_picture", "mobile_phone"]


class UserAddressForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        fields = ["country", "city", "street", "building", "apartment"]

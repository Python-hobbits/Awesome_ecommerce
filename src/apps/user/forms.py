from allauth.account.forms import SignupForm

from django import forms


class UserSignupForm(SignupForm):
    type = forms.ChoiceField(choices=[("Seller", "Seller"), ("Customer", "Customer")])

    def custom_signup(self, request, user):
        user.user_type = self.cleaned_data["type"]
        user.save()

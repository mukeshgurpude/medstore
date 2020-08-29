from allauth.account.forms import SignupForm
from django import forms


class UserSignUp(SignupForm):
    first_name = forms.CharField(max_length=10)
    last_name = forms.CharField(max_length=15)

    def signup(self, user):
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.save()
        return user

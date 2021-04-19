from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import UserProfile, SellerProfile


class UserForm(ModelForm):

    class Meta:
        model = User
        fields = ("first_name", "last_name")


class ProfileForm(ModelForm):

    class Meta:
        model = UserProfile
        exclude = ("user", )


class SellerForm(ModelForm):

    class Meta:
        model = SellerProfile
        exclude = ("user", )

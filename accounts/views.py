from django.shortcuts import render
from django.contrib.auth import get_user_model
# Create your views here.


def register_user(request):
    if request.method == "POST":
        pass
        # TODO: handle post data from signup form url: https://www.dev2qa.com/django-user-registration-and-login-use-built-in-authorization-example/ 3.2

    return render(request, "registration/signup.html")

from django.shortcuts import render
from .forms import UserForm, ProfileForm
from .models import UserProfile
from django.contrib.auth.decorators import login_required
import re
from django.contrib import messages
# Create your views here.


@login_required
def profile(request):

    if request.method == "POST":
        data = request.POST
        first = data.get("first_name", None)
        last = data.get("last_name", None)
        gender = data.get("gender", None)
        phone = data.get("phone", None)
        if not re.match("^\d{10}$", phone):
            messages.error(request, "Phone must be Numeric and 10 characters in length")
        else:
            user = request.user
            user.first_name = first
            user.last_name = last
            user.save()
            try:
                user.userprofile.gender = gender
                user.userprofile.phone = phone
                user.userprofile.save()
                user.save()
            except:
                profile = UserProfile(user=user, gender=gender, phone=phone)
                profile.save()

    user_data = UserForm(instance=request.user)
    profile_data = ProfileForm()
    try:
        if request.user.userprofile:
            profile_data = ProfileForm(instance=UserProfile.objects.get(user=request.user))
            has_profile = True
    except:
        has_profile = False
    ctx = {"user": user_data, "profile": profile_data, 'has_profile': has_profile}
    return render(request, "accounts/profile.html", ctx)

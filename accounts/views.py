import re
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.contrib.auth.models import Group
from django.contrib import messages
from .forms import UserForm, ProfileForm, SellerForm
from .models import UserProfile, SellerProfile
# Create your views here.


# noinspection PyArgumentList,PyArgumentList,PyArgumentList,PyArgumentList
@login_required
def profile(request: HttpRequest):
    """
    Handles profile changes and requests
    :param request: Request for profile details
    :type request: HttpRequest
    """
    if request.method == "POST":
        data = request.POST

        # data.get returns None by default ->
        first = data.get(key="first_name")
        last = data.get(key="last_name")
        gender = data.get(key="gender")
        phone = data.get(key="phone")

        if not re.match(r'^\d{10}$', phone):
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
            except ObjectDoesNotExist:
                prof = UserProfile(user=user, gender=gender, phone=phone)
                prof.save()

    user_data = UserForm(instance=request.user)
    profile_data = ProfileForm()
    seller = SellerForm()
    try:
        if request.user.userprofile:
            profile_data = ProfileForm(instance=UserProfile.objects.get(user=request.user))
            has_profile = True
        else:
            has_profile = False
    except ObjectDoesNotExist:
        has_profile = False
    try:
        seller = SellerForm(instance=request.user.sellerprofile)
    except ObjectDoesNotExist:
        pass
    ctx = {"user": user_data, "profile": profile_data, 'has_profile': has_profile,
           "is_seller": request.user.has_perm("medicines.add_medicine"), "seller": seller}
    return render(request, "accounts/profile.html", ctx)


@login_required
def be_seller(request):
    """
    Handles store details related data
    :type request: HttpRequest
    """
    if request.method == "POST":
        data = request.POST
        user = request.user
        store = data.get(key="store_name")
        address = data.get(key="address")
        pin = data.get(key="pincode")
        try:
            user.sellerprofile.store_name = store
            user.sellerprofile.address = address
            user.sellerprofile.pincode = pin
            user.sellerprofile.save()
            user.save()
            messages.success(request, "Your profile edited")
        except ObjectDoesNotExist:
            messages.success(request, "Congratulations! You are now seller at medstore")
            seller = SellerProfile(user=user, store_name=store, address=address, pincode=pin)
            seller.save()
        user.groups.add(Group.objects.get(name="Merchant"))
        user.save()
        return redirect("/profile/")

    seller = SellerForm()
    try:
        seller = SellerForm(instance=SellerProfile.objects.get(user=request.user))
    except ObjectDoesNotExist as e:
        print(e)

    ctx = {"seller": seller}
    return render(request, "accounts/apply.html", ctx)

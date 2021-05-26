# Manages authentication, user, profile, group related views
from typing import Dict, Union
from django.contrib.auth.models import User, Group
from django.http import JsonResponse
from django.http.request import HttpRequest
from accounts.forms import SellerForm
from accounts.models import UserProfile, SellerProfile
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth import (authenticate, login, logout)
from home.forms import UserSignUp
import re

# Update this variable to change the default data to be sent for the anonymous user
NotLoggedIn: Dict[str, Union[str, bool]] = {
    'username': 'anonymous',
    'loggedIn': False,
    'first_name': 'Anonymous',
    'last_name': ''
}


def get_current_user(request: HttpRequest) -> JsonResponse:
    """
    Get the details of current user

    :param request: GET request to get the current user data
    :type request: HttpRequest
    :return: User data
    :rtype: JsonResponse
    """
    if request.method != 'GET':
        return JsonResponse({'msg': 'Invalid request'}, status=400)

    if request.user.is_anonymous:
        return JsonResponse(NotLoggedIn, status=200)
    return JsonResponse(dict(username=request.user.username, full_name=request.user.get_full_name(),
                        short_name=request.user.get_short_name(), email=request.user.email,
                        loggedIn=not request.user.is_anonymous), status=200)


class ProfileView(LoginRequiredMixin, View):

    def get(self, request: HttpRequest) -> JsonResponse:
        """
        Return the current profile data, as json
        :param request: GET request to get the profile data
        :type request: HttpRequest
        :return: current profile details for the user
        :rtype: JsonResponse
        """
        # First check if the user has a profile configured, or else create a new profile
        try:
            p = self.request.user.userprofile
        except ObjectDoesNotExist:
            request.user.userprofile = UserProfile()
            p = request.user.userprofile
        data = dict()
        data['first_name'] = request.user.first_name
        data['last_name'] = request.user.last_name
        data['gender'] = p.gender
        data['phone'] = p.phone

        data['is_seller'] = bool(request.user.groups.filter(name='Merchant'))

        if data['is_seller']:
            data['store_name'] = request.user.sellerprofile.store_name
            data['address'] = request.user.sellerprofile.address
            data['pincode'] = request.user.sellerprofile.pincode

        return JsonResponse(data, status=200)

    def post(self, request: HttpRequest) -> JsonResponse:
        """
        Processes the formData to update the profile data in database

        :param request: POST data to update the profile
        :type request: HttpRequest
        :return: Responds if the data has been updated, or request failed
        :rtype: JsonResponse
        """
        data = self.request.POST
        phone = data.get("phone", '')

        if not re.match(r"^\d{10}$", phone):
            messages.error(request, "Phone number must be Numeric and 10 characters in length")
            return JsonResponse({"msg": "request failed with error",
                                 'err': "Phone number must be numeric and of 10 digits in length"})

        user: User = request.user
        user.first_name = data.get('first_name', '')
        user.last_name = data.get('last_name', '')
        user.save()
        try:
            user.userprofile.gender = data.get('gender', '')
            user.userprofile.phone = phone
            user.userprofile.save()
            user.save()
        except ObjectDoesNotExist:
            prof = UserProfile(user=user, gender=data.get('gender', ''), phone=phone)
            prof.save()

        return JsonResponse({'status': 'Data updated'}, status=200)


class SellerView(LoginRequiredMixin, View):

    def get(self, request):
        try:
            sp: SellerProfile = self.request.user.sellerprofile
            return JsonResponse({'is_seller': True, 'store_name': sp.store_name,
                                 'address': sp.address, 'pincode': sp.pincode}, status=200)
        except ObjectDoesNotExist:
            return JsonResponse({'is_seller': False}, status=400)

    def post(self, request):
        data = SellerForm(request.POST)
        try:
            if data.is_valid():
                post_data = request.POST

                p = SellerProfile(user=self.request.user,
                                  address=post_data['address'],
                                  store_name=post_data['store_name'],
                                  pincode=post_data['pincode'])
                p.save()
                self.request.user.groups.add(Group.objects.get(name='Merchant'))
                self.request.user.save()
                return JsonResponse({'msg': "You're seller now, maybe🤔"}, status=200)
        except TypeError as e:
            print(e)
        return JsonResponse({'msg': 'Invalid data', 'errors': data.errors}, status=400)


class APILoginView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        if self.request.user.is_anonymous:
            return JsonResponse({'loggedIn': False})
        return JsonResponse({'msg': 'already Logged in', 'loggedIn': True})

    def post(self, request: HttpRequest) -> JsonResponse:
        data = self.request.POST
        username = data['username']
        password = data['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'msg': 'Successfully logged In'})
        return JsonResponse({'msg': 'invalid credentials'})


def api_logout(request: HttpRequest):
    if request.user.is_anonymous:
        return JsonResponse({'msg': 'Invalid request'}, status=400)

    logout(request)
    return JsonResponse({'msg': 'Logged out successfully'}, status=200)


class APISignupView(View):
    """
    Custom signup view from scratch, implemented from scratch as I was unable to
    integrate json response property with the default view

    Will replace as soon as the response is generated by inheriting SignupView from
    `allauth.account.views`
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form = None
        self.user = None

    def get(self, request):
        self.form = UserSignUp()
        return JsonResponse({'msg': 'POST method required', 
                             'fields': list(self.form.fields.keys())}, status=400)

    def post(self, request: HttpRequest):
        """
        Post method for signup of the user

        :param request: a Http Post request
        :type request: HttpRequest
        :return: data whether the request was successful
        :rtype: JsonResponse
        """
        form = UserSignUp(request.POST)

        if form.is_valid():
            # Create a dummy user
            self.user = User.objects.create_user(username=form.clean_username(), email=form.clean_email())
            self.user.set_password(request.POST['password1'])
            form.signup(self.user)
            return JsonResponse({'msg': 'user created', 'id': self.user.id}, status=201)
        return JsonResponse({'msg': 'errors', 'errors': form.errors})

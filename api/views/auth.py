# Manages authentication, user, profile, group related views
from typing import Dict, Union
from django.http import JsonResponse
from django.http.request import HttpRequest
from accounts.models import UserProfile
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
# from accounts.forms import UserForm
from django.core.exceptions import ObjectDoesNotExist

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

    user = request.user

    if user.is_anonymous:
        return JsonResponse(NotLoggedIn, status=200)
    else:
        return JsonResponse(dict(username=request.user.username, full_name=request.user.get_full_name(),
                                 short_name=request.user.get_short_name(), email=request.user.email,
                                 loggedIn=not user.is_anonymous), status=200)


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
        form_data = request.POST
        # TODO: process this data
        return JsonResponse({})

# Manages authentication, user, profile, group related views
from django.http import JsonResponse
from django.http.request import HttpRequest
from django.core.serializers.json import Serializer
from accounts.models import UserProfile
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.forms import UserForm

NotLoggedIn = {
    'name': 'anonymous',
    'loggedIn': False
}


def get_current_user(request: HttpRequest) -> JsonResponse:
    """
    This function will return current user details in json format
    TODO: Add DocString
    """
    if request.method != 'GET':
        return JsonResponse({'msg': 'Invalid request'}, status=400)

    user = request.user

    if user.is_anonymous:
        return JsonResponse(NotLoggedIn, status=200)
    else:
        return JsonResponse({'full_name': request.user.get_full_name(),
                             'short_name': request.user.get_short_name(),
                             'email': request.user.email,
                             'loggedIn': not user.is_anonymous
                             }, status=200)


class ProfileView(LoginRequiredMixin, View):

    def get(self, request: HttpRequest) -> JsonResponse:
        """
        Return the current profile data, as json
        """
        # First check if the user has a profile configured, or else create a new profile
        try:
            p = self.request.user.userprofile
        except Exception:
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
        """
        form_data = request.POST
        print(self.request, request, form_data)
        # TODO: process this data
        return JsonResponse({})

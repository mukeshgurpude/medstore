# Manages authentication, user, profile, group related views
from django.http import JsonResponse


def get_current_user(request):
    """
    This function will return current user details in json format
    TODO: Add DocString
    """
    if request.method != 'GET':
        return JsonResponse({'msg': 'Invalid request'}, status=400)

    user = request.user

    if user.is_anonymous:
        return JsonResponse({'name': 'Anonymous', 'loggedIn': not user.is_anonymous}, status=200)
    else:
        return JsonResponse({'full_name': request.user.get_full_name(),
                             'short_name': request.user.get_short_name(),
                             'email': request.user.email,
                             'loggedIn': not user.is_anonymous
                             }, status=200)


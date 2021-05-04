from _ctypes_test import func
from functools import wraps
from django.test.client import Client
from django.http import JsonResponse
from django.contrib.auth.models import User


def check_response(path="/", login_required=True, method="GET", post_data=None) -> func:
    """
    Checks if response is returned and is json

    :param path: URL path to the destination
    :type path: str

    :param login_required: Specifies if login is required for the data
    :type login_required: bool

    :param method: HTTP method to check for the given url
    :type method: str

    :param post_data: Data for the POST request if the method is POST
    :type post_data: dict

    :rtype: func
    """
    if post_data is None:
        post_data = dict()

    def wrapper(function: func):
        @wraps(function)
        def run(*args, client=Client(), **kwargs):
            if login_required:
                data = {"username": "test_user_23589", "password": "test_password"}
                User.objects.create_user(**data)
                client.login(**data)
            if method == 'GET':
                res = client.get(path, follow=True)
            else:
                res = client.post(path, post_data)
            assert res.status_code == 200
            assert isinstance(res, JsonResponse)
            return function(*args, **kwargs)
        return run
    return wrapper

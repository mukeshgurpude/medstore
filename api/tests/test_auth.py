from django.test.client import Client
from django.test import TestCase
from django.http import JsonResponse
from django.contrib.auth.models import User


USER_CREDENTIALS = {
   "username": "newUser",
   "password": "myPasswordWith."
}


class ProfileTestCase(TestCase):
    def __init__(self, *args, **kwargs):
        super(ProfileTestCase, self).__init__(*args, **kwargs)
        self.failureException = ValueError
        self.longMessage = False

    def setUp(self) -> None:
        """
            Setup the test user, and log in with the test user to access the profile page
        """
        self.user = User.objects.create_user(**USER_CREDENTIALS)
        self.client.login(**USER_CREDENTIALS)

    def test_get_output(self):
        """
            Tests if the GET requests to profile are working and also returning the correct response
        """
        res = self.client.get('/api/v1/profile/')
        self.assertEqual(res.status_code, 200)  # Check if response is returned
        self.assertIsInstance(res, JsonResponse)  # check if json is returned

    def test_post_output(self):
        """
        Tests if the POST requests to profile are working and also returning the correct response
        """
        res = self.client.post('/api/v1/profile/')
        self.assertEqual(res.status_code, 200)  # Check if response is returned
        self.assertIsInstance(res, JsonResponse)  # check if json is returned

    # TODO: test the data
    # TODO: teardown

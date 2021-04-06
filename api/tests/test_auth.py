from django.test import TestCase
from django.http import JsonResponse
from django.contrib.auth.models import User
from api.decorators import check_response
from django.utils.decorators import method_decorator


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

    @method_decorator(check_response(path="/api/v1/user/"))
    def test_get_user(self):
        res: JsonResponse = self.client.get("/api/v1/user/")
        self.assertEqual(self.user.username, res.json()['username'])

        self.client.logout()
        res: JsonResponse = self.client.get("/api/v1/user/")
        self.assertEqual('anonymous', res.json()['username'])
        self.client.login(**USER_CREDENTIALS)

    @method_decorator(check_response(path="/api/v1/profile/"))
    def test_get_output(self):
        """
            Tests if the GET requests to profile are working and also returning the correct response
        """
        res = self.client.get('/api/v1/profile/')
        self.assert_('first_name' in res.json(), 'First name is not returned')
        self.assert_('last_name' in res.json(), 'Last name is not returned')
        self.assert_('phone' in res.json(), 'Phone number is not returned')
        self.assert_('gender' in res.json(), 'Gender is not returned')
        self.assert_('is_seller' in res.json(), 'Seller details are not returned')
        is_seller = res.json()['is_seller']
        self.assertIsInstance(is_seller, bool)

    @method_decorator(check_response(path="/api/v1/profile/", method="POST", post_data={}))
    def test_post_output(self):
        """
        Tests if the POST requests to profile are working and also returning the correct response
        """
        res: JsonResponse = self.client.post('/api/v1/profile/', {})
        # TODO: Test the POST output


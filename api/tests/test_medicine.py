from django.contrib.auth.models import User
from django.test import TestCase
from api.decorators import check_response
from django.utils.decorators import method_decorator

from api.tests.test_auth import USER_CREDENTIALS, STORE_DATA
from api.tests.utils import create_merchant
from medicines.models import Medicine, MedCat

NEW_Medicine = {
    'name': 'Dummy for testing',
    'price': 100.5,
    'category': 'fever',
    'description': 'This is intended for testing only',
    'quantity': 200
}


class TestCreateView(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(**USER_CREDENTIALS)

    def handle_permit(self, login=True):
        """
        Handles the permissions in case of this tests
        :param login: Specifies if, the user should be logged in
        :type login: bool
        """
        if login:
            self.client.login(**USER_CREDENTIALS)
        else:
            self.client.logout()

    @method_decorator(check_response(path="/api/v1/", login_required=False))
    def test_get_list(self):
        pass

    def test_new_add(self):
        """
        Test if the POST requests to create new medicines are working
        """
        # Create the necessary models
        create_merchant()
        m = MedCat.objects.create(name='fever')
        m.save()

        # Login
        self.handle_permit()
        res = self.client.post('/api/v1/', NEW_Medicine)
        self.assertEqual(res.status_code, 400, 'Non permitted users are allowed to use')

        # Become seller | Get permissions
        self.client.post('/api/v1/sell/', STORE_DATA)

        res = self.client.post('/api/v1/', {**NEW_Medicine, 'category': m.id})
        self.assertEqual(res.status_code, 201, res.json().get('errors', res.json().get('msg', 'No message')))
        self.assertTrue(Medicine.objects.filter(name=NEW_Medicine['name']), 'Medicine not created')

        # Check duplicate request
        res = self.client.post('/api/v1/', {**NEW_Medicine, 'category': m.id})
        self.assertEqual(res.status_code, 400, 'Duplicate medicines are being created')

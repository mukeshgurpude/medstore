from django.contrib.auth.models import User
from django.test import TestCase
from api.decorators import check_response
from django.utils.decorators import method_decorator
from api.tests.test_auth import USER_CREDENTIALS, STORE_DATA
from medicines.models import Medicine
from api.views.medicine import MedicineView
from django.http import QueryDict

NEW_Medicine = {
    'name': 'Dummy for testing',
    'price': 100.5,
    'category': 1,
    'description': 'This is intended for testing only',
    'quantity': 200
}


class TestMedViews(TestCase):
    # Initial data for testing
    fixtures = ['api/tests/med_initial.json']

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
        res = self.client.get('/api/v1/')
        self.assertEqual(Medicine.objects.count(), len(res.json()))

        query = QueryDict('price__lt=5')
        res = MedicineView.get_queryset(query)
        self.assertTrue(all(m.price <= 5 for m in res))

        query = QueryDict('category=Fever')
        res = MedicineView.get_queryset(query)
        self.assertTrue(all(m.category.name == 'Fever' for m in res))

    def test_new_add(self):
        """
        Test if the POST requests to create new medicines are working
        """

        # Login
        self.handle_permit()
        res = self.client.post('/api/v1/', NEW_Medicine)
        self.assertEqual(res.status_code, 400, 'Non permitted users are allowed to use')

        # Become seller | Get permissions
        self.client.post('/api/v1/sell/', STORE_DATA)

        res = self.client.post('/api/v1/', {**NEW_Medicine, 'category': 1})
        self.assertEqual(res.status_code, 201, 
                         res.json().get('errors', res.json().get('msg', 'No message')))
        self.assertTrue(Medicine.objects.filter(name=NEW_Medicine['name']), 'Medicine not created')

        # Check duplicate request
        res = self.client.post('/api/v1/', {**NEW_Medicine, 'category': 1})
        self.assertEqual(res.status_code, 400, 'Duplicate medicines are being created')

    @method_decorator(check_response("/api/v1/detail/1/", login_required=False))
    def test_detail_data(self):
        res = self.client.get("/api/v1/detail/new-med/")
        self.assertEqual(res.json()['name'], 'New Med')

    def test_update_med(self):
        res = self.client.post('/api/v1/detail/1/', {**NEW_Medicine, 'name': 'Dummy changed name'})
        self.assertEqual(res.json()['name'], 'Dummy changed name')
        self.assertEqual(Medicine.objects.get(pk=1).name, 'Dummy changed name')

from django.test import TestCase
from django.utils.decorators import method_decorator

from api.decorators import check_response


class TestBillingAddress(TestCase):

    fixtures = ["api/fixtures/" + file + ".json" for file in {"user"}]

    def setUp(self) -> None:
        self.credentials = {
            'id': 16,
            'username': 'demo_username',
            'password': 'demo_password'
        }
        self.client.login(**self.credentials)

    @method_decorator(check_response('/api/v1/address/'))
    def test_get(self):
        res = self.client.get('/api/v1/address/')
        self.assertIsInstance(res.json()['fields'], dict)

    def test_post(self):
        res = self.client.post('/api/v1/address/',
                               dict(address='Gajanan Residency', pincode=412105,
                               city='Alandi', landmark='Opposite Kaivalya Hostel'))
        self.assertFalse(res.json()['errors'])
        res = self.client.post('/api/v1/address/', dict(address='Gajanan Residency', pincode=412105,
                                city='Alandi', landmark='Near MIT Academy of Engineering'))
        self.assertTrue(res.json()['errors'])


class Test(TestCase):
    def test_get_stripe_conf(self):
        res = self.client.get('/conf/')
        self.assertEqual(res.status_code, 200)
        self.assertTrue('publicKey' in res.json())

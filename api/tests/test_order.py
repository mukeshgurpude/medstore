from django.test import TestCase
from django.utils.decorators import method_decorator

from api.decorators import check_response
from cart.models import Order


class TestOrderView(TestCase):

    fixtures = ["api/fixtures/" + file + ".json" for file in {"user", "ordered_orders",
                                                              "permissions", "med", "medCategory"}]

    def setUp(self) -> None:
        self.credentials = {
            'id': 16,
            'username': 'demo_username',
            'password': 'demo_password'
        }
        self.client.login(**self.credentials)

    @method_decorator(check_response('/api/v1/orders/'))
    def test_get(self):
        res = self.client.get('/api/v1/orders/')
        self.assertEqual(len(res.json()['orders']),
                         Order.objects.filter(user_id=self.credentials['id'],
                                              ordered=True).count())

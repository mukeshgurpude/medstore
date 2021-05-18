from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from api.decorators import check_response
from api.tests.test_auth import USER_CREDENTIALS
from cart.models import CartItem
from api.views import CartView

User = get_user_model()


class TestCart(TestCase):
    fixtures = ["api/fixtures/" + file + ".json" for file in {"user", "cartItem", "order",
                                                              "permissions", "med", "medCategory"}]

    def setUp(self) -> None:
        self.user = User.objects.create(**USER_CREDENTIALS)
        self.client.login(**USER_CREDENTIALS)
        self.credentials = {
            'username': 'demo_username',
            'password': 'demo_password'
        }
        self.cart_item = CartItem.objects.filter(user=self.user).first()

    @method_decorator(check_response('/api/v1/cart/'))
    def test_cart_list(self):
        res = self.client.get('/api/v1/cart/')
        self.assertEqual(len(res.json()['items']), 
                         CartItem.objects.filter(user=self.user.id).count())

        # Below details are of the user with cart items
        self.client.login(**self.credentials)
        res = self.client.get('/api/v1/cart/')
        self.assertEqual(len(res.json()['items']), CartItem.objects.filter(user=16).count())

    def test_cart_increase(self):
        current_quantity = self.cart_item.quantity if self.cart_item else 0
        CartView.update_item(pk=self.cart_item.item.id if self.cart_item else 4,
                             action='increase', user=self.user)
        self.cart_item = CartItem.objects.get(user=self.user)
        self.assertEqual(self.cart_item.quantity, current_quantity+1)

    def test_cart_full_update(self):
        # Increase 1 time, (add the item)
        CartView.update_item(pk=4, user=self.user, action='increase')
        self.assertEqual(len(CartItem.objects.filter(user=self.user)), 1)

        c = CartItem.objects.get(user=self.user)

        # Increase to 2
        CartView.update_item(pk=4, user=self.user, action='increase')
        c.refresh_from_db()
        self.assertEqual(c.quantity, 2)

        # Decrease back to 1
        CartView.update_item(pk=4, user=self.user, action='decrease')
        c.refresh_from_db()
        self.assertEqual(c.quantity, 1)

        # Delete the instance, as quantity is 0
        CartView.update_item(pk=4, user=self.user, action='decrease')
        self.assertEqual(len(CartItem.objects.filter(user=self.user)), 0)

    def test_add_new_to_cart(self):
        CartView.update_item(pk=4, user=self.user, action='increase')
        self.assertEqual(len(CartItem.objects.filter(user=self.user)), 1)

    def test_post_request(self):
        self.client.login(**self.credentials)
        self.client.post('/api/v1/cart/', {'id': 4, 'action': 'increase'})
        self.assertEqual(len(CartItem.objects.filter(user=16)), 2)

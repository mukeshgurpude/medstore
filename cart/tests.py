from django.test import TestCase
from cart.models import CartItem, Order
from django.contrib.auth.models import User
from medicines.models import Medicine, MedCat
# Create your tests here.


class AfterTestPayment(TestCase):
    test_user = None
    medcat = None
    med = None
    cart_item = None
    order = None

    def test_create_test_user(self):
        self.test_user = User.objects.create_user("Test_User", "testmail@mail.com", "MyPassword")
        self.client.login(username=self.test_user.username, password=self.test_user.password)
        self.assertIsNotNone(self.test_user.id)

    def test_create_med(self):
        self.test_create_test_user()
        self.medcat = MedCat.objects.create(name="test_category")
        self.med = Medicine.objects.create(name="test_medicine", category=self.medcat, price=24.12, quantity=454,
                                           description="Test_ Description", owner=self.test_user)
        self.assertIsNotNone(self.med.id)

    def test_create_cart_item(self):
        self.test_create_med()
        self.cart_item = CartItem.objects.create(item=self.med, user=self.test_user, quantity=4)
        self.assertEqual(self.cart_item.total_amount(), self.cart_item.item.price*self.cart_item.quantity)

    def test_create_order(self):
        self.test_create_cart_item()
        self.order = Order.objects.create(user=self.test_user)
        self.order.items.add(self.cart_item)

    def test_after_pay(self):
        self.test_create_order()
        self.cart_item.item.quantity -= self.cart_item.quantity
        self.order.ordered = True
        self.assertEqual(self.med.quantity, 450)

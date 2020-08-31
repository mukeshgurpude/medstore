from django.test import TestCase
from cart.models import CartItem, Order
from django.contrib.auth.models import User
from medicines.models import Medicine, MedCat
# Create your tests here.


class AfterPayment(TestCase):
    test_user = None
    medcat = None
    med = None
    cart_item = None
    order = None

    def create_test_user(self):
        self.test_user = User.objects.create_user("Test_User", "testmail@mail.com", "MyPassword")
        self.client.login(username=self.test_user.username, password=self.test_user.password)
        self.assertEqual(self.test_user, "")

    def create_med(self):
        self.medcat = MedCat.objects.create(name="test_category")
        self.med = Medicine.objects.create(name="test_medicine", category=self.medcat, price=24.12, quantity=454,
                                           description="Test_ Description", owner=self.test_user)

    def create_cart_item(self):
        self.cart_item = CartItem.objects.create(item=self.med, user=self.test_user, quantity=4)

    def create_order(self):
        self.order = Order.objects.create(user=self.test_user)
        self.order.items.add(self.med)

    def after_pay(self):
        pass

    def clear_all(self):
        self.test_user.delete()
        self.medcat.delete()
        self.med.delete()


if __name__ == '__main__':
    test = AfterPayment()
    test.create_test_user()

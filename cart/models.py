from django.db import models
from medicines.models import Medicine
from django.contrib.auth import get_user_model
# Create your models here.

user = get_user_model()


class CartItem(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    item = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} of {self.item}"

    def total_amount(self):
        return self.quantity * self.item.price


class Order(models.Model):
    items = models.ManyToManyField(CartItem)
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    orderID = models.CharField(null=True, max_length=16)
    paymentID = models.CharField(null=True, max_length=50)

    def __str__(self):
        return self.user.username

    def get_order_total(self):
        return sum([item.total_amount() for item in self.items.all()])

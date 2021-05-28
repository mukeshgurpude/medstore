from django.db import models
from medicines.models import Medicine
from django.contrib.auth import get_user_model
import json
# Create your models here.

user = get_user_model()


class CartItem(models.Model):
    objects = models.Manager()
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    item = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    purchased = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} of {self.item}"

    def total_amount(self):
        return float(self.quantity * self.item.price)

    @property
    def as_json(self):
        return {'id': self.id, 'quantity': self.quantity, 'total': self.total_amount()}


class Order(models.Model):
    objects = models.Manager()
    items = models.ManyToManyField(CartItem)
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    orderID = models.CharField(null=True, max_length=16)
    paymentID = models.CharField(null=True, max_length=50)
    orderDate = models.DateTimeField(null=True, auto_now=True)
    total = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    postOrder = models.CharField(null=True, max_length=200)

    def __str__(self):
        return f"Order of {self.order_total} by {self.user.username}"

    @property
    def order_total(self):
        if not self.ordered:
            return sum([item.total_amount() for item in self.items.all()])
        return self.total

    @property
    def as_json(self):
        if not self.ordered:
            return {item.item.name: item.as_json for item in self.items.all()}
        return json.loads(self.postOrder)

    def order_now(self):
        items = [item.as_json for item in self.items.all()]
        self.postOrder = json.dumps(items)
        self.total = sum([item.total_amount() for item in self.items.all()])
        self.save()

from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.


class BillingAddress(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    address = models.CharField(max_length=50, )
    pincode = models.PositiveIntegerField()
    city = models.CharField(max_length=20)
    landmark = models.CharField(max_length=30, null=True)

    def __str__(self):
        return f"{self.user.username} Billing Address"

    @property
    def as_json(self):
        return dict(address=self.address, pincode=self.pincode, city=self.city, landmark=self.landmark)

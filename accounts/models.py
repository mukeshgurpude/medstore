from django.db import models
from django.conf import settings
# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    gender = models.CharField(null=True,
                              choices=[("Male", "Male"), ("Female", "Female"),
                                       ("Prefer not to say", "Prefer not to say")],
                              max_length=50)
    phone = models.PositiveBigIntegerField(verbose_name="Mobile Number", null=True)

    def __str__(self):
        return self.user.username + " Profile"

    def full_name(self):
        """
        Full name of the user
        :return: Name of the user
        :rtype: str
        """
        return self.user.first_name + self.user.last_name


class SellerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    store_name = models.CharField(max_length=20, help_text="Your store name",
                                  verbose_name="Store Name")
    address = models.TextField(max_length=40, help_text="Your store address")
    pincode = models.IntegerField()

    def __str__(self):
        return "seller " + self.user.username + " Profile"

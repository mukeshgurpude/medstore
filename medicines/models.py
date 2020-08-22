from django.db import models
from django.conf import settings
# Create your models here.


class MedCat(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Medicine(models.Model):
    name = models.CharField(max_length=20)
    category = models.ForeignKey(MedCat, on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=5)
    quantity = models.IntegerField()
    thumbnail = models.BinaryField(null=True, editable=True, blank=True)
    thumb_content_type = models.CharField(max_length=256, null=True, blank=True, help_text="MIMEType for thumbnail")
    description = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

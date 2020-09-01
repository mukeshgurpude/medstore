from django.db import models
from django.conf import settings
import random, string
from django.core.validators import MinValueValidator
# Create your models here.


class MedCat(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Medicine Category"


class Medicine(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=20)
    category = models.ForeignKey(MedCat, on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=5)
    quantity = models.PositiveBigIntegerField()
    thumbnail = models.BinaryField(null=True, editable=True, blank=True)
    thumb_content_type = models.CharField(max_length=256, null=True, blank=True, help_text="MIMEType for thumbnail")
    description = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(default="".join(random.sample(str(name)+str(category.name)+str(price)[:-3], 15)), unique=True)

    def __str__(self):
        return self.name

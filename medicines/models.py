from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.conf import settings
import random
from django.utils.text import slugify


class MedCat(models.Model):
    objects = models.Manager()
    name: str = models.CharField(max_length=20)

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
    thumb_content_type = models.CharField(max_length=256, default='image/png', null=True,
                                          blank=True, help_text="MIMEType for thumbnail")
    description = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-price"]

    def save(self, *args, **kwargs):
        slug = slugify(self.name + '-' + self.category.name)
        while Medicine.objects.filter(slug=slug):
            slug = "".join(random.sample(slug, len(slug)))
        self.slug = slug
        super(Medicine, self).save(*args, **kwargs)

    @property
    def as_json(self):
        try:
            owner = self.owner.sellerprofile.store_name
        except ObjectDoesNotExist:
            owner = 'Medstore'
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category.name,
            'price': self.price,
            'quantity': self.quantity,
            'description': self.description,
            'owner': owner,
            'slug': self.slug
        }

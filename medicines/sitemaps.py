from django.contrib.sitemaps import Sitemap
from .models import Medicine
from django.urls import reverse


class MedSiteMap(Sitemap):
    priority = 0.9
    changefreq = "daily"

    def items(self):
        return Medicine.objects.all()

    def location(self, obj):
        return reverse("medicines:detail", args=(obj.id,))

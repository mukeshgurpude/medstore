"""
Sitemap views for medicines
"""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Medicine


class MedSiteMap(Sitemap):
    """
    Class to wrap up dynamic urls for medicines
    """
    priority = 0.9
    changefreq = "daily"

    def items(self):
        return Medicine.objects.all()

    def location(self, obj):
        return reverse("medicines:detail", args=(obj.id,))

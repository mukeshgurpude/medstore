""" 
Top level sitemap which generates sitemap for all static urls
(except which are generated elsewhere)
"""

from django.contrib import sitemaps
from django.urls import reverse


class StaticSitemap(sitemaps.Sitemap):
    """
    Url paths to static urls
    """
    changeFreq = 'monthly'
    priority = .8

    def items(self):
        pages = {
            "cart": ['home', 'my_orders'],
            "checkout": ['order'],
            "home": ['home'],
            "medicines": ["all"]
        }
        return [app + ":" + view for app, views in pages.items() for view in views]

    def location(self, page):
        return reverse(page)

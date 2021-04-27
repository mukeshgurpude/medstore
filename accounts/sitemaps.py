from django.contrib import sitemaps
from django.urls import reverse


class AccountSiteMap(sitemaps.Sitemap):
    priority = .5
    changeFreq = 'daily'

    def items(self):
        return ['profile', 'apply']

    def location(self, item):
        return reverse(f'Account:{item}')

"""
Sitemap classes related to the account related views
"""
from django.contrib import sitemaps
from django.urls import reverse


class AccountSiteMap(sitemaps.Sitemap):
    """
    Urls related to custom user model
    """
    priority = .5
    changeFreq = 'daily'

    def items(self):
        return ['profile', 'apply']

    def location(self, item):
        return reverse(f'Account:{item}')


class AllAuthSitemap(sitemaps.Sitemap):
    """
    Sitemap urls for allauth account urls
    """
    priority = .5
    changeFreq = 'monthly'
    
    def items(self):
        return ['login', 'logout']

    def location(self, item):
        return reverse(f"account_{item}")

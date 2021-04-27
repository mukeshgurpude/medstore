from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from medicines.sitemaps import MedSiteMap
from accounts.sitemaps import AccountSiteMap
from django.views.generic import TemplateView
from .sitemaps import StaticSitemap


sitemaps = {
    'accounts': AccountSiteMap,
    'medicines': MedSiteMap,
    'other': StaticSitemap
}

urlpatterns = [
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain"), name="robots"),
    path("sitemap.xml", sitemap, {'sitemaps': sitemaps}, name="sitemap_url"),
    path("", include("home.urls")),
    path("", include("cart.urls")),
    path('admin/', admin.site.urls),
    path('medicines/', include("medicines.urls")),
    path("", include("checkout.urls")),
    path("", include("accounts.urls")),
    path("", include("allauth.urls")),
    path("api/v1/", include("api.urls")),
]

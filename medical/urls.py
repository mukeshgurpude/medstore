"""medical URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from medicines.sitemaps import MedSiteMap
from django.views.generic import TemplateView


sitemaps = {
    'medicines': MedSiteMap
}

urlpatterns = [
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain"), name="robots"),
    path("sitemap.xml/", sitemap, {'sitemaps': sitemaps}, name="sitemap"),
    path("", include("home.urls")),
    path("", include("cart.urls")),
    path('admin/', admin.site.urls),
    path('medicines/', include("medicines.urls")),
    path("", include("checkout.urls")),
    # path("", include("django.contrib.auth.urls")),  # Builtins
    path("", include("accounts.urls")),
    path("", include("allauth.urls")),
]

from django.shortcuts import render
from django.views import View
from django.conf import settings
# Create your views here.


class HomeView(View):
    def get(self, request, ):
        ctx = {
            'installed': settings.INSTALLED_APPS,
        }
        return render(request, "home/main.html", ctx)

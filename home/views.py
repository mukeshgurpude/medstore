from django.shortcuts import render
from django.views import View
from django.conf import settings
# Create your views here.


class HomeView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dev_env = settings.DEBUG

    def get(self, request, ):
        ctx = {
            "Dev_Env": self.dev_env,
        }
        return render(request, "home/main.html", ctx)

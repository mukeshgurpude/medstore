from django.urls import path, include
from.views import HomeView

app_name = 'home'

urlpatterns = [
    path("", HomeView.as_view(), name='home')
]

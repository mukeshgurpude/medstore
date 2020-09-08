from django.urls import path
from .import views

app_name = "Account"

urlpatterns = [
    path("profile/", views.profile, name="profile"),
]

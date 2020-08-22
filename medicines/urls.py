from django.urls import path, reverse_lazy
from . import views

app_name = "medicines"

urlpatterns = [
    path("", views.MedListView.as_view(), name="all"),
]

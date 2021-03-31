from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('', views.MedicineView.as_view(), name="APIv1")
]

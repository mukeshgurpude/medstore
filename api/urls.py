from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('', views.MedicineView.as_view(), name="APIv1"),
    path('user/', views.get_current_user, name="user"),
    path('add/', views.CreateView.as_view(), name='medicine_add')
]

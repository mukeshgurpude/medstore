from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    # Medicines
    path('', views.MedicineView.as_view(), name="APIv1"),
    path('add/', views.CreateView.as_view(), name='medicine_add'),

    # Regarding user details
    path('user/', views.get_current_user, name="user"),
    path('profile/', views.ProfileView.as_view(), name="profile"),
]

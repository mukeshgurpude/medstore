from django.urls import path
from api import views

app_name = 'api'

urlpatterns = [
    # Medicines
    path('', views.MedicineView.as_view(), name="APIv1"),
    path('detail/<int:pk>/', views.APIDetailView.as_view(), name="medicine_detail"),
    path('detail/<str:slug>/', views.APIDetailView.as_view(), name="medicine_detail"),

    # Regarding user details
    path('user/', views.get_current_user, name="user"),
    path('profile/', views.ProfileView.as_view(), name="profile"),
    path('login/', views.APILoginView.as_view(), name="login"),
    path('logout/', views.api_logout, name="logout"),
    path('register/', views.APISignupView.as_view(), name='register'),
    path('sell/', views.SellerView.as_view(), name='sell'),

    # Cart, Orders related views
    path('cart/', views.CartView.as_view(), name='cart'),
    path('orders/', views.OrderView.as_view(), name='orders'),
    path('address/', views.APIBillingAddress.as_view(), name='orders'),
]

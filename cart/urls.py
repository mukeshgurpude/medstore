from django.urls import path
from .views import cartview, add_to_cart, remove_from_cart
from . import views

app_name = "cart"

urlpatterns = [
    path("cart/", cartview, name="home"),
    path("add/<slug>", add_to_cart, name="add"),
    path("remove/<slug>", remove_from_cart, name="remove"),
    path("increase/<slug>", views.increase_cart_test, name="increase"),
    path("decrease/<slug>", views.decrease_cart_test, name="decrease"),
    path("orders/", views.order_view, name="my_orders")
]

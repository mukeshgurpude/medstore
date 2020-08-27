from django.urls import path
from .views import cartview, add_to_cart, remove_from_cart

app_name = "cart"

urlpatterns = [
    path("cart/", cartview, name="home"),
    path("add/<slug>", add_to_cart, name="add"),
    path("remove/<slug>", remove_from_cart, name="remove")
]

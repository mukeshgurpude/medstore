from django.urls import path
from .views import checkout_view, payment, create_checkout_session, stripe_conf

app_name = "checkout"

urlpatterns = [
    path("order/", checkout_view, name="order"),
    path("pay/", payment, name="pay"),
    path("new/", create_checkout_session, name="test"),
    path("conf/", stripe_conf, name="conf"),
]

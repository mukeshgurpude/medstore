from django.urls import path
from .views import checkout_view, payment, create_checkout_session, stripe_conf, stripe_webhook
from . import views

app_name = "checkout"

urlpatterns = [
    path("order/", checkout_view, name="order"),
    path("pay/", payment, name="pay"),
    path("new/", create_checkout_session, name="test"),
    path("conf/", stripe_conf, name="conf"),
    path("hook/", stripe_webhook, name="webhook"),
    path("success/", views.success, name="success"),
    path("cancelled/", views.fail, name="fail"),
]

from django.contrib import admin
from .models import Order, CartItem
# Register your models here.

admin.site.register(Order)
admin.site.register(CartItem)

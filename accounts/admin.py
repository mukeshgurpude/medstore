from django.contrib import admin
from .models import UserProfile, SellerProfile
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(SellerProfile)

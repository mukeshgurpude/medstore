from django.contrib import admin
from .models import MedCat, Medicine
# Register your models here.


class Setup(admin.ModelAdmin):
    list_display = ["name", "price"]
    fieldsets = [
        ("Basic", {"fields": ["name", "price", "thumbnail", "category", ]}),
        ("Quantity", {"fields": ["quantity", "description", ]})
    ]
    search_fields = ["name"]
    list_filter = ["category", "name", "owner"]


admin.site.register(Medicine, Setup)

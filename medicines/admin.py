from django.contrib import admin
from .models import MedCat, Medicine
# Register your models here.


class Setup(admin.ModelAdmin):
    list_display = ["name", "price", "category"]
    fieldsets = [
        ("Basic", {"fields": ["name", "price", "category", ]}),
        ("Quantity", {"fields": ["quantity", "description", "owner"]}),
        ("View", {"fields": ["thumbnail", "thumb_content_type"]})
    ]
    search_fields = ["name", "description", ]
    list_filter = ["category", "owner"]


admin.site.register(Medicine, Setup)
admin.site.register(MedCat)

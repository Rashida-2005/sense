from django.contrib import admin
from .models import Product, Sale
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.
admin.site.register(Product)
admin.site.register(Sale)
admin.site.register(CustomUser, UserAdmin)

class SaleAdmin(admin.ModelAdmin):
    readonly_fields = ("total",)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Product, Sale, CustomUser

# Register Product
admin.site.register(Product)

# Register Sale with custom admin
class SaleAdmin(admin.ModelAdmin):
    readonly_fields = ("total",)
admin.site.register(Sale, SaleAdmin)

# Register CustomUser with custom admin
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'role', 'is_staff', 'is_active']
    list_filter = ("role", "is_staff", "is_active")
    search_fields = ("username","email", "role")
    fieldsets = UserAdmin.fieldsets + (("Custom Fields", {"fields": ("role",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (("Custom Fields", {"fields": ("role",)}),)

admin.site.register(CustomUser, CustomUserAdmin)

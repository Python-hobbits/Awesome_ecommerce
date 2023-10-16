from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from src.apps.user.models import User, UserProfile, UserAddress


class UserAdminExtended(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("User Type", {"fields": ("user_type",)}),)
    list_filter = ("user_type",)


admin.site.register(User, UserAdminExtended)
admin.site.register(UserProfile)
admin.site.register(UserAddress)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from src.apps.user.models import User, UserProfile


class UserAdminExtended(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("User Type", {"fields": ("user_type",)}),)


admin.site.register(User, UserAdminExtended)
admin.site.register(UserProfile)

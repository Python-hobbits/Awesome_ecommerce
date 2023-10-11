from django.contrib import admin

from src.apps.user.models import User, UserProfile, UserAddress


# class UserAdminExtended(UserAdmin):
#     fieldsets = UserAdmin.fieldsets + (("User Type", {"fields": ("user_type","user_profile")}),)
#     list_filter = ("user_type","user_profile")


admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(UserAddress)

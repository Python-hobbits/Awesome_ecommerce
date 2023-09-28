from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from src.apps.user.models import User, UserProfile


admin.site.register(User, UserAdmin)
admin.site.register(UserProfile)

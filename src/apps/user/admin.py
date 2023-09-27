from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from src.apps.user.models import User


admin.site.register(User, UserAdmin)

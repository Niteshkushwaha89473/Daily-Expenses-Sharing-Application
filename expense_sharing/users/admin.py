from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('id', 'username', 'email', 'password', 'mobile_no','first_name', 'last_name')  # Ensure proper commas

admin.site.register(CustomUser, CustomUserAdmin)
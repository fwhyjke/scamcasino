from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


# Реализация модели User для админки
class CustomUserAdmin(UserAdmin):
    model = User
    ordering = ['username']
    list_display = ['username', 'is_superuser']
    list_filter = ('username',)


admin.site.register(User, CustomUserAdmin)

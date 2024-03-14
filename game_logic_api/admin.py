from django.contrib import admin
from django.contrib.auth.models import User
from .models import UserBalance


class UserBalanceAdmin(admin.ModelAdmin):
    model = UserBalance
    ordering = ['user']
    list_display = ['user', 'balance', 'record']
    list_filter = ('record', 'balance')


admin.site.register(UserBalance, UserBalanceAdmin)

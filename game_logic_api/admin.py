from django.contrib import admin
from .models import UserBalance


# Регистрируем таблицу балансов пользователя в админку
class UserBalanceAdmin(admin.ModelAdmin):
    model = UserBalance
    ordering = ['user']
    list_display = ['user', 'balance', 'record']
    list_filter = ('record', 'balance')


admin.site.register(UserBalance, UserBalanceAdmin)

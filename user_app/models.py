from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from user_app.managers import UserManager


# Кастомная модель пользователя. Решил так сделать, так как мне не нужно иметь кучу лишних полей, ибо тут это нужно
# только для возможности позже создать таблицу либеров BlackJack
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True, max_length=20)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['is_superuser']
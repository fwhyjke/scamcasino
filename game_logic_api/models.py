from django.db import models
from user_app.models import User


# Класс для определения модели баланса пользователя в БД. Из полей - пользователь в отношения 1 к 1, баланс и личный рек
class UserBalance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.PositiveSmallIntegerField(default=5000)
    record = models.PositiveIntegerField(default=5000)

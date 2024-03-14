from django.db import models
from user_app.models import User


class UserBalance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.PositiveSmallIntegerField(default=5000)
    record = models.PositiveIntegerField(default=5000)

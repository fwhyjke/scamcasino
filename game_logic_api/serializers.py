from rest_framework import serializers
from rest_framework.serializers import Serializer


class BalanceSerializer(Serializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    balance = serializers.IntegerField(default=5000)
    record = serializers.IntegerField(default=5000)
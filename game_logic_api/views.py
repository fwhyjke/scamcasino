from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.views import APIView

from game_logic_api.models import UserBalance
from game_logic_api.serializers import BalanceSerializer

from game_logic_api.logic import Coinflip


class GetUserBalanceAPI(APIView):
    def get(self, request):
        user = request.query_params.get('id')
        balance_object = UserBalance.objects.get(user=user)
        balance = dict(BalanceSerializer(balance_object).data)
        if balance['balance'] > balance['record']:
            balance_object.record = balance['balance']
            balance_object.save()
        return Response(balance['balance'])


class ResetBalanceAPI(APIView):
    def get(self, request):
        user = request.query_params.get('id')
        balance_object = UserBalance.objects.get(user=user)
        balance_object.balance = 5000
        balance_object.save()
        return Response({"message": "Баланс успешно сброшен"})


class GameProcessAPI(APIView):
    def get(self, request):
        user = request.query_params.get('id')
        bet = request.query_params.get('bet')
        balance_object = UserBalance.objects.get(user=user)
        if Coinflip():
            balance_object.balance = balance_object.balance + int(bet)
            balance_object.save()
        else:
            balance_object.balance = balance_object.balance - int(bet)
            balance_object.save()
        return Response({"message": "Игра завершина"})

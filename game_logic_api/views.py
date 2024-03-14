from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.views import APIView

from game_logic_api.models import UserBalance
from game_logic_api.serializers import BalanceSerializer


class GetUserBalanceAPI(APIView):
    def get(self, request):
        user = request.query_params.get('id')
        balance_object = UserBalance.objects.get(user=user)
        balance = dict(BalanceSerializer(balance_object).data)
        if balance['balance'] > balance['record']:
            balance_object.record = balance['balance']
            balance_object.save()
        return Response(balance['balance'])

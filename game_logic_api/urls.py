from django.urls import path
from game_logic_api.views import *

urlpatterns = [
    path('user-balance', GetUserBalanceAPI.as_view(), name='balance'),
    path('reset-balance', ResetBalanceAPI.as_view(), name='reset'),
    path('start-game', StartGameAPI.as_view(), name='start'),
    path('player-turn', PlayerTurnAPI.as_view(), name='player-turn'),
    path('lose', PlayerLoseAPI.as_view(), name='player-lose'),
    path('refund', PlayerRefundAPI.as_view(), name='player-ref'),
    path('reduce-balance', ReduceBalance.as_view(), name='reduce-bal'),
    path('dealer-turn', DealerTurn.as_view(), name='dealer-turn'),
    path('result', ResultGameAPI.as_view(), name='result'),
    path('stop', PlayerStop.as_view(), name='stop'),
]

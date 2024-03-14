from django.urls import path
from game_logic_api.views import *

urlpatterns = [
    path('user-balance', GetUserBalanceAPI.as_view(), name='balance'),
    path('reset-balance', ResetBalanceAPI.as_view(), name='reset'),
    path('start-game', GameProcessAPI.as_view(), name='bet'),
]

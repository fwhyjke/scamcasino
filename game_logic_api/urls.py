from django.urls import path
from game_logic_api.views import *

urlpatterns = [
    path('user-balance', GetUserBalanceAPI.as_view(), name='balance'),
]

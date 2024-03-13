from django.urls import path
from blackjack.views import *

urlpatterns = [
    path('', ShowPageView.as_view(), name='welcome'),
]
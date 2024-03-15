from blackjack.views import *
from django.urls import path

# Настройка маршрутизации (все основные ссылки на сайте)
urlpatterns = [
    path('', StartView.as_view(), name='welcome'),
    path('login', UserLoginView.as_view(), name='login'),
    path('registration', UserRegistrationView.as_view(), name='registration'),
    path('game', GameView.as_view(), name='game'),
    path('logout', UserLogoutView.as_view(), name='logout'),
]

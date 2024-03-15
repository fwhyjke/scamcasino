from django.contrib import messages
from django.contrib.auth import login

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView
from blackjack.forms import *


# Класс для отображения приветственной страницы. Никакой логики на нем нет, поэтому достаточно TemplateView
class StartView(TemplateView):
    template_name = 'blackjack/index.html'


# Класс для страници входа пользователей. Наследуется от удобного для этого класса LoginView
class UserLoginView(LoginView):
    template_name = 'blackjack/login.html'
    form_class = LoginForm

    # В случае удачного входа отправляем на страницу с игрой
    def get_success_url(self):
        return reverse_lazy('game')

    # Проверка валидности данных
    def form_invalid(self, form):
        messages.error(self.request, 'Неверная почта или пароль')
        return super().form_invalid(form)


# Класс для регистрации пользователей.
class UserRegistrationView(CreateView):
    template_name = 'blackjack/registration.html'
    model = User
    form_class = RegistrationForm
    success_url = reverse_lazy('game')

    # Если пользователь зарегистрирован, переводим на страницу с игрой под его аккаунтом
    def form_valid(self, form):
        user = form.save()
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(self.request, user)
        return redirect('game')


# Класс для выхода пользователь. Не имеет своей страницы.
class UserLogoutView(LogoutView):
    next_page = reverse_lazy('login')


# Класс для отображения страницы игры. Сам класс простой, тк основные взаимодействия происходят через DRF, redis и JS.
class GameView(LoginRequiredMixin, TemplateView):
    template_name = 'blackjack/game.html'
    login_url = 'login'

    # Передача текущего пользователя в шаблон для удобного взаимодействия через JS.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


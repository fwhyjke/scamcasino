from django.contrib import messages
from django.contrib.auth import login

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView
from blackjack.forms import *


class StartView(TemplateView):
    template_name = 'blackjack/index.html'


class UserLoginView(LoginView):
    template_name = 'blackjack/login.html'
    form_class = LoginForm

    def get_success_url(self):
        return reverse_lazy('game')

    def form_invalid(self, form):
        messages.error(self.request, 'Неверная почта или пароль')
        return super().form_invalid(form)


class UserRegistrationView(CreateView):
    template_name = 'blackjack/registration.html'
    model = User
    form_class = RegistrationForm
    success_url = reverse_lazy('game')

    def form_valid(self, form):
        user = form.save()
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(self.request, user)
        return redirect('game')


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('login')


class GameView(LoginRequiredMixin, TemplateView):
    template_name = 'blackjack/game.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user  # Передача текущего пользователя в шаблон
        return context

